import ast
from os import environ
from urllib.parse import unquote_plus

import boto3


def lambda_handler(event, context):
    _ = context
    s3 = boto3.client('s3')
    sns_msg = ast.literal_eval(event['Records'][0]['Sns']['Message'])
    record = sns_msg['Records'][0]
    source_bucket = str(record['s3']['bucket']['name'])
    source_key = str(unquote_plus(record['s3']['object']['key']))
    new_bucket = environ['BUCKET']
    new_prefix = environ.get('PREFIX', '')
    if not source_key.endswith('/'):
        key = source_key.split('/')[-1]
        print(
            f'Copying s3://{source_bucket}/{source_key}'
            f' to s3://{new_bucket}/{new_prefix}{key}.'
        )
        s3.copy_object(
            Bucket=new_bucket,
            Key=f'{new_prefix}{key}',
            CopySource={
                'Bucket': source_bucket,
                'Key': source_key
            }
        )
