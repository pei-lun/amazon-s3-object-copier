# Copy Created S3 Object

Require: Python 3.6

An AWS Lambda function copying S3 object to another S3 bucket when receiving object created event from SNS.

E.g., after s3://source/foo/bar created, it will be copied to s3://destination/foo/bar with `TARGET_BUCKET` and `PREFIX` environment variables set to _destination_ and _foo/_.
