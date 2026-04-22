import boto3

def get_lambda_functions(region="us-east-1"):
    client = boto3.client("lambda", region_name=region)
    response = client.list_functions()

    results = []

    for fn in response["Functions"]:
        results.append({
            "resource_type": "lambda",
            "resource_id": fn["FunctionName"],
            "region": region,
            "metadata": {
                "runtime": fn["Runtime"],
                "last_modified": fn["LastModified"]
            }
        })

    return results