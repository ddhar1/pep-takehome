"""
- Create APIs to allow querying the DynamoDB table. Endpoints could include:
  - Fetch records for a specific site and time range.
  - Retrieve all anomalies for a given site.
- Use any framework of your choice (e.g., FastAPI, Flask).
"""
from aws_lambda_wsgi import handle_request
from boto3.dynamodb.conditions import Key
from boto3 import resource
from datetime import datetime
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

dynamodb = resource('dynamodb')
table_name = os.environ["DYNAMODB_TABLE"]

table = dynamodb.Table(table_name)

@app.route('/data_by_site_timerange', methods=['GET'])
def get_data_by_timerange():
    site_id = request.args.get('site_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    # Validate parameters
    if not start_time or not end_time or not site_id:
        return jsonify({
            'error': 'Missing required parameters: site_id, start_time or end_time'
        }), 400

    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)    
    except ValueError:
        return jsonify({
            'error': 'Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
        }), 400
        
    if end_dt < start_dt:
        return jsonify({
            'error': 'end_time must be greater than start_time'
        }), 400
    
    start_epoch = round(start_time.timestamp())
    end_epoch = round(end_time.timestamp())

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(int(item_id)) & Key('timestamp').between(start_epoch, end_epoch)
        )
        
        return jsonify({
            'count': response['Count'],
            'items': response['Items']
        })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500


def lambda_handler(event, context):
    return handle_request(app, event, context)


if __name__ == '__main__':
    app.run(debug=True)