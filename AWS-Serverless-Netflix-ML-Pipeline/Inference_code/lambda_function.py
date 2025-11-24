import boto3
import csv
import io
import os
import uuid
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "")
TABLE_NAME = os.environ.get("TABLE_NAME", "")

def simple_classifier(row):
    """
    Heuristic classifier using engineered features.
    You can replace this with real model logic if needed.
    """
    def to_int(x, default=0):
        try:
            return int(x)
        except:
            return default

    duration_num = to_int(row.get("duration_num", 0))
    has_season_word = to_int(row.get("has_season_word", 0))
    is_US = to_int(row.get("is_US", 0))
    is_India = to_int(row.get("is_India", 0))

    # Simple scoring model
    score = 0
    score += 2 * has_season_word
    if duration_num >= 120:
        score += 1
    if is_India:
        score += 1
    if is_US and duration_num < 100:
        score -= 1

    return "TV Show" if score >= 1 else "Movie"

def lambda_handler(event, context):
    """
    Input example:
    {
      "bucket": "pooja-netflix-processed-data",
      "key": "clean/netflix_titles_clean.csv"
    }
    """
    bucket = event.get("bucket", PROCESSED_BUCKET)
    key = event.get("key", "clean/netflix_titles_clean.csv")

    print(f"Running inference on s3://{bucket}/{key}")

    # 1. Read cleaned CSV
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(body))
    rows = list(reader)

    if not rows:
        return {"statusCode": 200, "body": "No rows to predict."}

    # 2. Add predictions
    for row in rows:
        row["prediction"] = simple_classifier(row)

    # 3. Write predictions CSV back to S3
    pred_key = key.replace("clean/", "predictions/").replace("_clean.csv", "_predictions.csv")
    out_buffer = io.StringIO()
    writer = csv.DictWriter(out_buffer, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

    s3.put_object(
        Bucket=bucket,
        Key=pred_key,
        Body=out_buffer.getvalue().encode("utf-8")
    )

    # 4. Log summary to DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    run_id = str(uuid.uuid4())
    item = {
        "run_id": run_id,
        "processed_bucket": bucket,
        "clean_key": key,
        "prediction_key": pred_key,
        "num_records": len(rows),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    table.put_item(Item=item)

    print(f"Saved predictions to s3://{bucket}/{pred_key}")
    print(f"Logged run {run_id} to DynamoDB table {TABLE_NAME}")

    return {
        "statusCode": 200,
        "body": f"Predictions saved to {bucket}/{pred_key}, run_id={run_id}"
    }