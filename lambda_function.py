import json
from os import environ
from urllib.parse import unquote_plus

import boto3


def lambda_handler(event, *_):
    new_bucket = environ['BUCKET']
    new_prefix = environ.get('PREFIX', '')
    recursive = environ.get('RECURSIVE', '0')
    skip = environ.get('SKIP', '')

    record: dict = event['Records'][0]
    if record.get('EventSource') == 'aws:sns':
        s3_event = json.loads(record['Sns']['Message'])
        if s3_event.get('Event') == 's3:TestEvent':
            return
        source_bucket = s3_event['Records'][0]['s3']['bucket']['name']
        source_key = unquote_plus(s3_event['Records'][0]['s3']['object']['key'])
    elif record.get('eventSource') == 'aws:s3':
        source_bucket = record['s3']['bucket']['name']
        source_key = unquote_plus(record['s3']['object']['key'])
    else:
        print(f'Unrecognized event: "{event}".')
        return

    s3_client = boto3.client('s3')
    if not source_key.endswith('/'):
        new_key = generate_new_key(
            source_key,
            prefix=new_prefix,
            recursive=bool(int(recursive)),
            skip=skip,
        )
        print(
            f'Copying object from s3://{source_bucket}/{source_key} to s3://{new_bucket}/{new_key}.'
        )
        s3_client.copy_object(
            Bucket=new_bucket,
            Key=new_key,
            CopySource={'Bucket': source_bucket, 'Key': source_key},
        )


def generate_new_key(key, prefix='', recursive=False, skip=''):
    if prefix != '' and not prefix.endswith('/'):
        raise InvalidPrefix
    if skip != '' and not skip.endswith('/') and recursive:
        raise InvalidPrefix
    stripped_key = key[len(skip) :]
    base_key = stripped_key if recursive else stripped_key.split('/')[-1]
    return f'{prefix}{base_key}'


class InvalidPrefix(Exception):
    def __str__(self):
        return 'Invalid prefix!'
