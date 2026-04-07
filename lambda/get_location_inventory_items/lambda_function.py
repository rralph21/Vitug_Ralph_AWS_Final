import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.getenv("TABLE_NAME", "InventoryApp"))

    # Validate path param
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter")
        }

    location_id = int(event["pathParameters"]["id"])

    try:
        response = table.query(
            IndexName="GSI_SK_PK",
            KeyConditionExpression=Key("location_id").eq(location_id)
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []))
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }