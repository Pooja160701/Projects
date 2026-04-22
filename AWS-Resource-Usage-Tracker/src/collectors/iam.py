import boto3

def get_iam_users():
    iam = boto3.client("iam")
    response = iam.list_users()

    results = []

    for user in response["Users"]:
        results.append({
            "resource_type": "iam",
            "resource_id": user["UserName"],
            "region": "global",
            "metadata": {
                "create_date": str(user["CreateDate"])
            }
        })

    return results