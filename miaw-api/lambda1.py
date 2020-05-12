import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    datos= dynamodb.Table('NOMBRE DE LA TABLA')
    items = datos.scan()

    return {
        'statusCode': 200,
        'body': items
    }