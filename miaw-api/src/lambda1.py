import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.client import ClientError

dynamodb = boto3.resource('dynamodb')
    #Nombre de la tabala
datos= dynamodb.Table('animal_adoption')

def lambda_handler(event, context):
    
    try:
        # Query
        data=event['queryStringParameters']['pk']
        items2 = datos.query(
            KeyConditionExpression=Key('PK').eq(data)
        )
        return {
            'statusCode': 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
    }
    except ClientError:
        return {
            'statusCode': 500,
            'body': 'Error querying database',
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }