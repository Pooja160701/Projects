import json
import boto3
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from collectors.ec2 import get_ec2_instances
from collectors.s3 import get_s3_buckets
from collectors.lambda_func import get_lambda_functions
from collectors.iam import get_iam_users


def safe_collect(func):
    try:
        return func()
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


def lambda_handler(event, context):

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(safe_collect, [
            get_ec2_instances,
            get_s3_buckets,
            get_lambda_functions,
            get_iam_users
        ]))

    # Flatten all results
    all_resources = []
    for result in results:
        all_resources.extend(result)

    # Add timestamp to each record
    timestamp = datetime.utcnow().isoformat()

    for r in all_resources:
        r["timestamp"] = timestamp

    # Convert to JSON lines format (Athena-friendly)
    json_lines = "\n".join(json.dumps(r) for r in all_resources)

    s3 = boto3.client("s3")
    bucket_name = "aws-resource-tracker-pooja"

    key = f"bronze/date={datetime.utcnow().strftime('%Y-%m-%d')}/data.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json_lines,
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "body": "Data lake updated successfully"
    }