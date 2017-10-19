# Amazon S3 Object Copier

Require: Python 3.6

An AWS Lambda function copying S3 object to another S3 bucket when receiving object created event from SNS.

## Environment Variables

- `BUCKET`: (required) Destination bucket
- `PREFIX`: (optional) Prefix prepended to object key
- `RECURSIVE`: (optional)
- `SKIP`: (optional)

## Usage

After `s3://source/bar/baz/object` created, it will be copied to `s3://destination/foo/object` with `BUCKET` set to `destination` and `PREFIX` set to `foo/`. If `RECURSIVE` is set to `1`, the object will be copied to `s3://destination/foo/bar/baz/object`. You can set `SKIP` to `bar/` and the object will be copied to `s3://destination/foo/baz/object`.

## Test

Run `pip install -r requirements-test.txt` and then run `pytest`.
