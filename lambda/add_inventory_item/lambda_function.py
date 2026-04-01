import json
import boto3
import os
import ulid

def lambda_handler(event, context):
    try:
        body = event.get("body", "{}")
        data = json.loads(body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid JSON format.")
        }

    required_fields = ["name", "description", "qty", "price", "location_id"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {
            "statusCode": 400,
            "body": json.dumps(f"Missing required field(s): {', '.join(missing_fields)}")
        }

    table_name = os.getenv("TABLE_NAME", "InventoryApp")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        # Generate ULID instead of UUID
        unique_id = str(ulid.new())

        item = {
            "id": unique_id,
            "name": str(data["name"]),
            "description": str(data["description"]),
            "qty": int(data["qty"]),
            "price": float(data["price"]),
            "location_id": int(data["location_id"])
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Item added successfully.",
                "item": item
            })
        }

    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps("qty, price, and location_id must be valid numbers.")
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error adding item: {str(e)}")
        }