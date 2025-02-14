"""
- An Quick Flask API service that allows you to query dynamodb
    for data for a site_id, within a time range

Example query:
http://localhost:5000/data_by_site_timerange?site_id=5&start_time=2025-02-13T09:20:00&end_time=2025-02-13T09:30:00
"""
from datetime import datetime, timezone
from decimal import Decimal
from math import floor, ceil
import os
from boto3 import resource
from boto3.dynamodb.conditions import Key
from boto3_helpers.dynamodb import query_table
from flask import Flask, request, jsonify

app = Flask(__name__)
iso_format2 = '%Y-%m-%dT%H:%M:%S'

dynamodb = resource('dynamodb')
table_name = "SitesEnergyStatsDB" # TODO - would be nicer if we could access variable created in tf file

table = dynamodb.Table(table_name)

@app.route('/', methods=['GET'])
def home():
    return "Please query using data_by_site_timerange\n"
    "Example: localhost:5000/data_by_site_timerange?site_id=1."
    "Use  Use ISO format (YYYY-MM-DDTHH:MM:SS)"

def decimal_to_float_values(d: dict) -> dict:
    """DynamoDB stores floats as Decimals 
        Given a dictionary that is expected from the Dynamo DB
            returns the dictionary but with all Decimal values
            for the keys  converted to Float valuess
    """
    output = {}
    #for k in [ 'energy_consumed_kwh', 'energy_generated_kwh', 'net_energy_kwh', 'anomoly']:
    for k in d.keys():
        output[k] = float(d[k]) if isinstance(d[k], Decimal) else d[k]
    return output


@app.route('/data_by_site_timerange', methods=['GET'])
def get_data_by_timerange():
    """
    get:
      summary: Returns a user by ID.
      parameters:
        - in: site_id
          description: Site ID wanted to be queried
        - in: start_time
          description: start_time in format: %Y-%m-%dT%H:%M:%S
        - in: end_time
          description: end_time in format: %Y-%m-%dT%H:%M:%S
      responses:
        200:
          description:
          schema: 
            type: object
            properties:
              time:
                type: object
                example: {
                    'energy_consumed_kwh': 10,
                    'energy_generated_kwh': 11
                    'net_energy_kwh': 1,
                     'anomoly': False
                }

    TODO: rest of responses
    """
    site_id = request.args.get('site_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Validate parameters
    if not start_time or not end_time or not site_id:
        return jsonify({
            'error': 'Missing required parameters: site_id, start_time or end_time'
        }), 400

    try:
        start_dt = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({
            'error': 'Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
        }), 400
    print(end_dt, start_dt)
    if end_dt < start_dt:
        return jsonify({
            'error': 'end_time must be greater than start_time'
        }), 400

    start_epoch = floor(start_dt.timestamp())
    end_epoch = ceil(end_dt.timestamp())

    try:
        print("between", start_epoch, end_epoch)
        # ugly code
        output = { 
            datetime.utcfromtimestamp(
                float(item['timestamp'])).strftime(iso_format2): 
            decimal_to_float_values(item) for 
                                        item in 
                                        query_table(
                                            table, 
                                    KeyConditionExpression=Key('site_id').eq(int(site_id)) & \
                                            Key('timestamp').between(start_epoch, end_epoch))
            }

    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

    if len(output) == 0:
        return jsonify(f"Your query of site_id: {site_id} and timestamp"
        F" between {start_time} and {end_time} returned no results")

    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)