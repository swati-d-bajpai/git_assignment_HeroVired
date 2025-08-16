import boto3
from botocore.exceptions import ClientError

def lambda_handler(event=None, context=None):
    s3 = boto3.client("s3")
    unencrypted_buckets = []

    # List all buckets
    buckets = s3.list_buckets()

    for bucket in buckets.get("Buckets", []):
        bucket_name = bucket["Name"]
        if not bucket_name.startswith("swati"):
            continue
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc["ServerSideEncryptionConfiguration"]["Rules"]
            if rules:
                print(f"Bucket {bucket_name} has encryption enabled.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                print(f"Bucket {bucket_name} does NOT have encryption enabled.")
                unencrypted_buckets.append(bucket_name)
            else:
                print(f"Error checking bucket {bucket_name}: {e}")

    print("Unencrypted Buckets:", unencrypted_buckets)
    return {"unencrypted_buckets": unencrypted_buckets}


if __name__ == "__main__":
    # Run locally as a normal script
    result = lambda_handler()
    print("Result:", result)
