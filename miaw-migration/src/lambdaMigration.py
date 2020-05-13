import boto3
from urllib.parse import unquote_plus
import io
import pandas as pd


s3_client = boto3.client('s3')


def lambda_handler(event, context):
   for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        keylave = unquote_plus(record['s3']['object']['key'])
        print()
        if keylave.count(".csv")==1:
            object_file = s3_client.get_object(Bucket=bucket, Key=keylave)
            tamano=pd.read_csv(object_file['Body'])
            print(tamano.shape[0])
            for i in range(0,tamano.shape[0]):
                lista=list(range(0,tamano.shape[0])) 
                lista.remove(i)
                object_file2 = s3_client.get_object(Bucket=bucket, Key=keylave)
                initial_df = pd.read_csv(object_file2['Body'],skiprows=[0,2,3,4,5])
                print(initial_df)
        else:
            copy_source = { 
                'Bucket': bucket, 
                'Key': keylave
            } 
            archi='media/'
            tpkey=archi+keylave
            s3_client.copy_object(Bucket='upb-convert-image-lambda-lab-level1',CopySource=copy_source, Key=tpkey)
            print(bucket,keylave)