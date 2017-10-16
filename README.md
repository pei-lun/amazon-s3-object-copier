# Amazon S3 Object Copier

Require: Python 3.6

An AWS Lambda function copying S3 object to another S3 bucket when receiving object created event from SNS.

## Environment Variables

- `BUCKET`: required.
- `PREFIX`: required.
- `RECURSIVE`: optional.
- `SKIP`: optional.

## Usage

After `s3://source/x/y/object` created, it will be copied to `s3://destination/z/object` with `BUCKET` set to `destination` and `PREFIX` set to `z/`. If `RECURSIVE` set to `1`, the object will be copied to `s3://destination/x/y/z/object`. You can set `SKIP` to `x/` and the object will be copied to `s3://destination/y/z/object`.