"""
2. Data Processing
- Process each uploaded file using an AWS Lambda function.
- For each record in the JSON file:
  - Calculate `net_energy_kwh` = `energy_generated_kwh` - `energy_consumed_kwh`.
  - Identify anomalies where:
    - `energy_generated_kwh < 0`
    - `energy_consumed_kwh < 0`.
"""

from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3 import resource
from collections import namedtuple
import json
import logging
import os
from decimal import Decimal, Inexact, Rounded

logger = logging.getLogger()
logger.setLevel("INFO")

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[Rounded] = 0

table_name = os.environ["DYNAMODB_TABLE"]

bucket_key = namedtuple('bucket_key', ["bucket_name", "key_name"])

s3 = resource('s3')
dynamodb = resource("dynamodb")

def lambda_handler(event, context):
    bucket_key_trigger = serialize_event_data(event) # get bucket name and file key 

    if not bucket_key_trigger:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No bucket or key info found? found"})
        }
    try:
        content_object = s3.Object(bucket_key_trigger.bucket_name, bucket_key_trigger.key_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
    except Exception as E:
        print("Error when finding or getting bucket/key: ", bucket_key_trigger)
        print(E)
        raise E
    site_data = json.loads(file_content)

    if len(site_data) == 0:
        # no data- maybe raise error?
        return

    table = dynamodb.Table(table_name)

    print(f"JSON has {len(site_data)} records")
    records_added = 0
    for site_datum in site_data:
        try:
            site_datum['energy_generated_kwh'] = Decimal(round(site_datum['energy_generated_kwh'], 2))
            site_datum['energy_consumed_kwh'] = Decimal(round(site_datum['energy_consumed_kwh'], 2))
            site_datum['net_energy_kwh'] = Decimal(round(site_datum['energy_generated_kwh'] - site_datum['energy_consumed_kwh']))
            site_datum['anomoly'] = True if site_datum['energy_generated_kwh'] < 0 or site_datum['energy_consumed_kwh'] < 0 else False

            table.put_item(Item=site_datum)
            records_added += 1
        except Exception as E:
            print(f"received {E} when parsing record from file: ", bucket_key_trigger)
            continue
    if len(site_data) != records_added:
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": f"{records_added} items out of {len(site_data)} "
                        f"records saved. Failed to save {len(site_data)-records_added}"})
        }
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"All {records_added} items saved"})
        }





def serialize_event_data(json_data) -> bucket_key:
    """
    Extract bucket name and file key from json_data - which should be s3 trigger
    Will fail if there are more than one items in key 'Records',
        or if looks like the event is not from s3 Put trigger

    """
    if len(json_data['Records']) > 1:
        raise ValueError("Multiple records found - application can't support this yet")
    for record in json_data['Records']:
        if record.get('eventSource') != 'aws:s3' or ('s3' not in record.keys()):
            raise ValueError("Expected eventSource to be from aws:s3, and it is", record['eventSource'])
        if record.get('eventName') != "ObjectCreated:Put":
            raise ValueError("Expected event name ObjectCreated:Put. It is", record['eventName'])
        
        bucket_name = record['s3']["bucket"]["name"]
        s3_key = record["s3"]["object"]["key"]
        print("S3 Key:", s3_key)
        print("bucket name: ", bucket_name)
        bucket_key_trigger = bucket_key(bucket_name, s3_key)
    
        #s3_data_size = json_data["Records"][0]["s3"]["object"]["size"]
    
    return bucket_key_trigger