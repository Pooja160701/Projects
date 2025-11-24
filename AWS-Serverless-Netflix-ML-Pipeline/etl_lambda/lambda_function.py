import boto3
import csv
import io
import os

s3 = boto3.client("s3")
PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "")

def encode_rating(r):
    mapping = {
        "TV-Y": 1, "TV-Y7": 1, "TV-G": 1,
        "TV-PG": 2, "PG": 2,
        "TV-14": 3, "PG-13": 3,
        "R": 4, "TV-MA": 4,
        "NC-17": 5
    }
    return mapping.get(r, 0)

def parse_duration(d):
    if not d:
        return 0
    parts = d.split()
    try:
        num = int(parts[0])
    except:
        return 0

    if "min" in d:
        return num
    if "Season" in d:
        return num * 60
    return num

def lambda_handler(event, context):
    record = event["Records"][0]
    src_bucket = record["s3"]["bucket"]["name"]
    src_key = record["s3"]["object"]["key"]

    print(f"Triggered by s3://{src_bucket}/{src_key}")

    # Download raw CSV
    obj = s3.get_object(Bucket=src_bucket, Key=src_key)
    raw = obj["Body"].read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)

    output_rows = []

    for row in rows:
        # Skip required missing fields
        if not row.get("release_year") or not row.get("duration") or not row.get("description"):
            continue

        # Feature engineering
        rating_enc = encode_rating(row.get("rating"))
        duration_num = parse_duration(row.get("duration"))
        title_length = len(row.get("title", ""))
        description_length = len(str(row.get("description", "")))
        has_season_word = 1 if "Season" in row.get("duration", "") else 0
        is_kids = 1 if row.get("rating") in ["TV-Y", "TV-Y7", "TV-G"] else 0

        country = row.get("country", "")
        is_US = 1 if "United States" in country else 0
        is_India = 1 if "India" in country else 0

        # Add cleaned row
        output_rows.append({
            "show_id": row["show_id"],
            "release_year": row["release_year"],
            "rating_enc": rating_enc,
            "duration_num": duration_num,
            "title_length": title_length,
            "description_length": description_length,
            "has_season_word": has_season_word,
            "is_kids": is_kids,
            "is_US": is_US,
            "is_India": is_India
        })

    # Build the clean output file key
    clean_key = f"clean/{src_key.split('/')[-1].replace('.csv', '_clean.csv')}"

    # Write output CSV buffer
    out_buffer = io.StringIO()
    writer = csv.DictWriter(out_buffer, fieldnames=output_rows[0].keys())
    writer.writeheader()
    writer.writerows(output_rows)

    # Upload cleaned CSV
    s3.put_object(
        Bucket=PROCESSED_BUCKET,
        Key=clean_key,
        Body=out_buffer.getvalue().encode("utf-8")
    )

    print(f"Saved cleaned file to s3://{PROCESSED_BUCKET}/{clean_key}")

    # RETURN what Step Functions needs
    return {
        "processed_bucket": PROCESSED_BUCKET,
        "clean_key": clean_key
    }