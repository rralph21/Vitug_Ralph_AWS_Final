import json
import boto3
import os
import uuid
from decimal import Decimal

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('InventoryApp')

    try:
        # Handle body parsing - could be string or already parsed dict
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
        
        new_item = {
            'id': str(uuid.uuid4()),
            'location_id': Decimal(str(body['location_id'])),
            'name': body['name'],
            'description': body['description'],
            'qty': Decimal(str(body['qty'])),
            'price': Decimal(str(body['price']))
        }

        table.put_item(Item=new_item)

        clean_item = json.loads(json.dumps(new_item, default=str))
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Item added successfully.",
                "Item": clean_item
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