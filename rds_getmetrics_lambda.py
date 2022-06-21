import json
import boto3
import datetime

cloudwatch = boto3.resource('cloudwatch')
s3 = boto3.resource('s3')

metric = cloudwatch.Metric('AWS/RDS','CPUUtilization')

def lambda_handler(event, context):
    s3_bucket_name = 'rds-cw-metrics' # Replace with your bucket name
    rds_instance_identifier = 'mysql-test2' # Replace with your DB identifier
    
    dimensions = [
        {
        "Name": "DBInstanceIdentifier",
        "Value": rds_instance_identifier},
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
    datapoints = response["Datapoints"]
    for datapoint in datapoints:
        datapoint["Timestamp"] = datapoint["Timestamp"].strftime("%m/%d/%Y, %H:%M:%S")
    
    data = json.dumps(datapoints)
    
    startTimeStr = startTime.strftime("%m-%d-%Y_%H-%M-%S")
    endTimeStr = endTime.strftime("%m-%d-%Y_%H-%M-%S")
    filename = 'rds-cpu-metrics_' + startTimeStr + '_' + endTimeStr + '.json'
    s3object = s3.Object(s3_bucket_name,  filename)

    s3object.put(
        Body=(bytes(data.encode('UTF-8')))
    )
    
    return data
