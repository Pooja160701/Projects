import boto3

def get_s3_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    results = []

    for bucket in response["Buckets"]:
        results.append({
            "resource_type": "s3",
            "resource_id": bucket["Name"],
            "region": "global",
            "metadata": {
                "creation_date": str(bucket["CreationDate"])
            }
        })

    return results