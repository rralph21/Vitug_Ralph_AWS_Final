import json
import boto3
import os

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = os.getenv('TABLE_NAME', 'InventoryApp')

    params = event.get("pathParameters", {})

    if "id" not in params or "location_id" not in params:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' or 'location_id' path parameter")
        }

    item_id = params["id"]
    location_id = params["location_id"]

    try:
        dynamo_client.delete_item(
            TableName=table_name,
            Key={
                "id": {"S": item_id},
                "location_id": {"N": str(location_id)}
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Item {item_id} at location {location_id} deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }