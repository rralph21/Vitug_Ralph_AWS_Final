import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Get Inventory Item - GET
    """
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    try:
        # Handle path parameters - could be None or missing
        path_params = event.get('pathParameters') or {}
        id = path_params.get('id')
        
        if not id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
                },
                'body': json.dumps({'error': 'Missing id parameter'})
            }

        response = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
                },
                'body': json.dumps("Item not found")
            }

        clean_item = json.loads(json.dumps(items[0], default=str))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,DELETE'
            },
            'body': json.dumps(clean_item)
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