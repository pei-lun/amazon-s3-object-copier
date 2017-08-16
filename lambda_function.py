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
    recursive = environ.get('RECURSIVE', '0')
    trimmed = environ.get('TRIMMED', '')
    if not source_key.endswith('/'):
        new_key = generate_new_key(
            source_key,
            new_prefix=new_prefix,
            recursive=bool(int(recursive)),
            old_prefix=trimmed
        )
        print(
            f'Copying object from s3://{source_bucket}/{source_key}'
            f' to s3://{new_bucket}/{new_key}.'
        )
        s3.copy_object(
            Bucket=new_bucket,
            Key=new_key,
            CopySource={
                'Bucket': source_bucket,
                'Key': source_key
            }
        )


def generate_new_key(key, new_prefix='', old_prefix='', recursive=False):
    if new_prefix != '' and not new_prefix.endswith('/'):
        raise InvalidPrefix()
    if old_prefix != '' and not old_prefix.endswith('/') and recursive:
        raise InvalidPrefix()
    trimmed_key = key[len(old_prefix):]
    base_key = trimmed_key if recursive else trimmed_key.split('/')[-1]
    return f'{new_prefix}{base_key}'


class InvalidPrefix(Exception):
    def __str__(self):
        return 'Invalid prefix!'
