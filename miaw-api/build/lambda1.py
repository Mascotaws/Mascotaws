import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table= dynamodb.Table('pets')
    data=event['queryStringParameters']['Dato']
    response = table.query(
        KeyConditionExpression=Key('pk').eq(data)
    )
    items = response['Items']
    for item in items:
        print(item)