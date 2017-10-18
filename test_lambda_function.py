import boto3
import pytest
from moto import mock_s3

from lambda_function import InvalidPrefix, generate_new_key, lambda_handler


def test_generate_new_key():
    old_key = 'bar/baz/object'
    skip = 'bar/'
    new_prefix = 'foo/'
    invalid_prefix = 'foo'
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, prefix=invalid_prefix)
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, recursive=True, skip=invalid_prefix)
    assert generate_new_key(old_key) == 'object'
    assert generate_new_key(
        old_key, prefix=new_prefix) == 'foo/object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            recursive=True) == 'foo/bar/baz/object'
    # skip argument only works when recursive argument set to True.
    assert generate_new_key(old_key, skip=skip) == 'object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            skip=skip) == 'foo/object'
    assert generate_new_key(old_key, recursive=True, skip=skip) == 'baz/object'
    assert generate_new_key(old_key, prefix=new_prefix, recursive=True,
                            skip=skip) == 'foo/baz/object'


@mock_s3
def test_lambda_handler(monkeypatch):
    source_bucket = 'source'
    source_key = 'bar/baz/object'
    object_content = b'Hello World'
    destination_bucket = 'destination'
    destination_key = 'foo/baz/object'
    sns_msg = (
        f'{{"Records": [{{"s3": {{"bucket": {{"name": "{source_bucket}"}},'
        f' "object": {{"key": "{source_key}"}}}}}}]}}'
    )
    event = {
        'Records': [
            {
                'EventSource': 'aws:sns',
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'event_subscription_arn',
                'Sns': {
                    'Type': 'Notification',
                    'MessageId': 'message_id',
                    'TopicArn': 'topic_arn',
                    'Subject': 'Amazon S3 Notification',
                    'Message': sns_msg,
                    'Timestamp': '2017-10-17T01:35:48.774Z',
                    'SignatureVersion': '1',
                    'Signature': 'signature',
                    'SigningCertUrl': 'signing_cert_url',
                    'UnsubscribeUrl': 'unsubscribe_url',
                    'MessageAttributes': {}
                }
            }
        ]
    }
    monkeypatch.setenv('BUCKET', destination_bucket)
    monkeypatch.setenv('PREFIX', 'foo/')
    monkeypatch.setenv('RECURSIVE', '1')
    monkeypatch.setenv('SKIP', 'bar/')
    s3_resource = boto3.resource('s3', region_name='us-east-1')
    s3_resource.create_bucket(Bucket=source_bucket)
    s3_resource.create_bucket(Bucket=destination_bucket)
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=source_bucket, Key=source_key,
                         Body=object_content)
    lambda_handler(event)
    copied_object = s3_resource.Object(destination_bucket, destination_key)
    assert object_content == copied_object.get()['Body'].read()
