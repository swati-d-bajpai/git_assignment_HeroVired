import boto3
from datetime import datetime, timezone, timedelta
import os

def lambda_handler(event, context):
    # Configure
    bucket_name = os.environ.get("BUCKET_NAME", "your-bucket-name")
    days_threshold = int(os.environ.get("DAYS_THRESHOLD", 1))

    s3 = boto3.client("s3")
    # threshold_date = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    threshold_date = datetime.now(timezone.utc) - timedelta(minutes=1)

    deleted_files = []

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if "Contents" not in response:
        print(f"No files found in bucket: {bucket_name}")
        return {"deleted": deleted_files}

    for obj in response["Contents"]:
        key = obj["Key"]
        last_modified = obj["LastModified"]

        if last_modified < threshold_date:
            s3.delete_object(Bucket=bucket_name, Key=key)
            deleted_files.append(key)
            print(f"Deleted: {key}")

    print(f"Deleted {len(deleted_files)} old files.")
    return {"deleted": deleted_files}
