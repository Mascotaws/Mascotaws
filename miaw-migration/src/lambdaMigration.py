import boto3
from urllib.parse import unquote_plus
import io
import pandas as pd
import json
import os


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
mascotatable = dynamodb.Table('animal_adoption')


def lambda_handler(event, context):
   for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        keylave = unquote_plus(record['s3']['object']['key'])
        if keylave.count(".csv")==1:
            object_file = s3_client.get_object(Bucket=bucket, Key=keylave)
            df=pd.read_csv(object_file['Body'])
            df.to_json(r'/tmp/file.json')
            with open('/tmp/file.json', 'r') as f:
                data = json.load(f)
            final_list = [{} for _ in next(iter(data.values()))]
            for att in data:
                count = 0
                for element in data[att]:
                    final_list[count][att] = data[att][element]
                    count+=1
            jsonlist=[]
            for song in final_list:
                if song['SK'].count("img")==1:
                    parte1= {
                        "PK":song['PK'],
                        "SK":song['SK'],
                        "PET_TYPE":song['PET_TYPE'],
                        "HEALTH":song['HEALTH'],
                        "AGE":song['AGE'],
                        "LOCATION":song['LOCATION'],
                    }
                    jsonlist.append(parte1)
                else:
                    parte2= {
                        "PK":song['PK'],
                        "SK":song['SK'],
                        "IMGORIGINAL":"media/"+song['IMG_ORIGINAL'],
                        "IMGNORMAL":"normal/"+song['IMG_ORIGINAL'],
                        "IMGTHUMB":"thumbnails/"+song['IMG_ORIGINAL'],
                    }
                    jsonlist.append(parte1)
            with mascotatable.batch_writer() as batch:
                for student in jsonlist:
                    batch.put_item(
                        Item=student
                    )
            print("Done!")
        else:
            copy_source = { 
                'Bucket': bucket, 
                'Key': keylave
            } 
            archi='media/'
            tpkey=archi+keylave
            s3_client.copy_object(Bucket='upb-convert-image-lambda-lab-level1',CopySource=copy_source, Key=tpkey)
            print(bucket,keylave)