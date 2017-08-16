# Copy Created S3 Object

Require: Python 3.6

An AWS Lambda function copying S3 object to another S3 bucket when receiving object created event from SNS.

## Environment Variables

- `BUCKET`: required.
- `PREFIX`: required.
- `RECURSIVE`: optional.
- `SKIP`: optional.

## Usage

After _s3://source/foo/bar/object_ created, it will be copied to _s3://destination/hello/world/object_ with `BUCKET` and `PREFIX` environment variables set to _destination_ and _hello/world/_.

If `RECURSIVE` set to _1_, the object will be copied to _s3://destination/hello/world/foo/bar/object_. You can set `SKIP` to _foo/_ and the object will be copied to _s3://destination/hello/world/bar/object_.
