import boto3
import json
import os

def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = os.getenv("TABLE_NAME", "InventoryApp")

    params = event.get("pathParameters", {})

    if "id" not in params or "location_id" not in params:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' or 'location_id' path parameter")
        }

    item_id = params["id"]
    location_id = params["location_id"]

    try:
        response = dynamo_client.get_item(
            TableName=table_name,
            Key={
                "id": {"S": item_id},
                "location_id": {"N": str(location_id)}
            }
        )

        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps("Item not found")
            }

        return {
            "statusCode": 200,
            "body": json.dumps(item, default=str)
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }