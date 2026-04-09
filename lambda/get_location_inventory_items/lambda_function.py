import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Get Location Inventory Items
    """
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    try:
        # Handle path parameters - could be None or missing
        path_params = event.get('pathParameters') or {}
        location_id = path_params.get('id')
        
        if not location_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
                },
                'body': json.dumps({'error': 'Missing location_id parameter'})
            }
        
        location_id = int(location_id)

        response = table.query(
            IndexName='GSI_SK_PK',
            KeyConditionExpression=Key('location_id').eq(location_id)
        )

        items = response.get('Items', [])
        clean_items = json.loads(json.dumps(items, default=str))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps(clean_items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps(str(e))
        }