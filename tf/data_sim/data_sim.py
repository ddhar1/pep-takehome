"""
- Continuously upload JSON files containing this data to an S3 bucket every 5 minutes.
- `site_id` (string): Unique identifier for a site.
- `timestamp` (string): UTC timestamp of the record.
- `energy_generated_kwh` (float): Energy generated in kWh.
- `energy_consumed_kwh` (float): Energy consumed in kWh.

"""
from datetime import datetime
import json
from os import getenv
from random import seed, uniform
import boto3

bucket_name = getenv('AWS_BUCKET_NAME', 'dd-peptakehome')
path = getenv("SITE_DATA_FILE_PREFIX",'raw/site_flow/')
iso_format = '%Y-%m-%dT%H%M%S'
seed(5)

def lambda_handler(event, context):
    """
    Generates data and places it in S3
    """
    s3 = boto3.resource('s3')

    now = datetime.utcnow() #

    date_path_str = now.strftime("%Y/%m/%d")
    now_str = now.strftime(iso_format)
    filename = path + f'{date_path_str}/' + f'{now_str}.json'
    print("Will save data to this file", filename)

    s3object = s3.Object(bucket_name, filename)

    output = generate_sites_data(now)
    print("Generated file output, of length", len(output))
    s3object.put(
        Body=(bytes(json.dumps(output).encode('UTF-8')))
    )


def generate_sites_data(now: datetime) -> list[dict]:
    """
    Generates a array of dicts 
    containing randomly generated energy generation/consumption data \
    for 20 different site IDs

    :now:  datetime data is being generated for
    """
    num_sites = 20

    data_for_sites = []

    for site_id in range(1, num_sites+1):
        d = {'site_id': site_id}
        d['timestamp'] = round(now.timestamp())
        d['energy_generated_kwh'] = round(uniform(-400, 40*100), 2)
        d['energy_consumed_kwh'] = round(uniform(-500, d['energy_generated_kwh']), 2)
        data_for_sites.append(d)

    return data_for_sites