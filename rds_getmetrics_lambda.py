import json
import boto3
import datetime

cloudwatch = boto3.resource('cloudwatch')
metric = cloudwatch.Metric('AWS/RDS','CPUUtilization')

def lambda_handler(event, context):
    dimensions = [
        {
        "Name": "DBInstanceIdentifier",
        "Value": "mysql-test2"},
        ]
    frequency = datetime.timedelta(hours=2)
    endTime=datetime.datetime.now()
    startTime = endTime - frequency
    period=300
    statistics = ['Average']
    unit= 'Percent'

    response = metric.get_statistics(
        Dimensions=dimensions,
        StartTime=startTime,
        EndTime=endTime,
        Period=period,
        Statistics=statistics,
        Unit=unit
        )
    result = response["Datapoints"][0]["Average"]
    return json.dumps(result)