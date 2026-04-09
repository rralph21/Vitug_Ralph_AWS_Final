import boto3
import json
import os

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(os.getenv("TABLE_NAME", "InventoryApp"))

    try:
        path_params = event.get('pathParameters') or {}
        item_id = path_params.get('id')

        if not item_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing id parameter'})
            }

        response = table.get_item(
            Key={'id': item_id}
        )

        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }