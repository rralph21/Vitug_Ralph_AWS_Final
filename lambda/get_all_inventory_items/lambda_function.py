import boto3
import json
import os

def lambda_handler(event, context):
    table_name = os.getenv("TABLE_NAME", "InventoryApp")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }