import json
import os
import time
import boto3
from datetime import datetime
from random import choice as random

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("RECEIPTS_TABLE", "pizza_orders_receipts")
table = dynamodb.Table(table_name)
deliver_names = ["Alice", "Bob", "chxmxii", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah"]

def lambda_handler(event, context):
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            order_id = record["messageAttributes"]["OrderID"]["stringValue"]
            restaurant = body.get("restaurant")
            customer = body.get("customer")
            pizza_type = body.get("pizza_type")
            pizza_size = body.get("pizza_size")
            address = body.get("address")

            timestamp = datetime.now(datetime.timezone.utc).isoformat()

            receipt = {
                "order_id": order_id,
                "timestamp": timestamp,
                "address": address,
                "client_name": customer,
                "delivery_name": f"{random(deliver_names)} 🛵",
                "restaurant": restaurant,
                "pizza_type": pizza_type,
                "size": pizza_size,
            }

            table.put_item(Item=receipt)
            print(f"Saved receipt for order_id={order_id}")

        except Exception as e:
            print(f"Failed to process record: {e}")
            continue

    return {"statusCode": 200, "body": "Processed"}