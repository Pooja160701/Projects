import json
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Parse SNS message
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Extract instance ID
    instance_id = message['Trigger']['Dimensions'][0]['value']

    # Reboot EC2
    ec2.reboot_instances(InstanceIds=[instance_id])

    return {
        "statusCode": 200,
        "body": f"Rebooted {instance_id}"
    }