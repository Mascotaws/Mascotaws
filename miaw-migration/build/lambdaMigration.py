import boto3
from urllib.parse import unquote_plus
import io
import pandas as pd
import json
import os


s3_client = boto3.client('s3')


def lambda_handler(event, context):
   for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        keylave = unquote_plus(record['s3']['object']['key'])
        if keylave.count(".csv")==1:
            object_file = s3_client.get_object(Bucket=bucket, Key=keylave)
            df=pd.read_csv(object_file['Body'])
            s3_client.put_object(Bucket=bucket, Key='datos.json')
            object_json = s3_client.get_object(Bucket=bucket, Key='datos.json')
            df.to_json(object_json['Body'])
            with open(object_json['Body'], 'r') as f:
                data = json.load(f)
                print(data)
            final_list = [{} for _ in next(iter(data.values()))]
            
        else:
            copy_source = { 
                'Bucket': bucket, 
                'Key': keylave
            } 
            archi='media/'
            tpkey=archi+keylave
            s3_client.copy_object(Bucket='upb-convert-image-lambda-lab-level1',CopySource=copy_source, Key=tpkey)
            print(bucket,keylave)