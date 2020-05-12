import boto3
from urllib.parse import unquote_plus


s3_client = boto3.client('s3')


def lambda_handler(event, context):
   for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        keylave = unquote_plus(record['s3']['object']['key'])
        copy_source = { 
            'Bucket': bucket, 
            'Key': keylave
        } 
        archi='media/'
        tpkey=archi+keylave
        s3_client.copy_object(Bucket='upb-convert-image-lambda-lab-level1',CopySource=copy_source, Key=tpkey)
        print(bucket,keylave)
        
        
        
        
        
        
        