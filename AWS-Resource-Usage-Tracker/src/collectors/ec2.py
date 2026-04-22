import boto3

def get_ec2_instances(region="us-east-1"):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances()

    results = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            results.append({
                "resource_type": "ec2",
                "resource_id": instance.get("InstanceId"),
                "region": region,
                "metadata": {
                    "instance_type": instance.get("InstanceType"),
                    "state": instance.get("State", {}).get("Name"),
                    "launch_time": str(instance.get("LaunchTime"))
                }
            })

    return results