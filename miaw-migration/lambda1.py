import os
import json
def handler(event, context):
    USER = os.getenv('MY_NAME')
    return {
        "statusCode": 200,
        "body": json.dumps("someData")
    }