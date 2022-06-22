# cloudwatch-metrics-export
CFN template for exporting CloudWatch metrics to S3

By default, CloudWatch Metrics do not have the native capability to export to S3. This CFN Template uses EventBridge and Lambda to dump metrics into an S3 bucket every hour for your EC2 or RDS instances. 
