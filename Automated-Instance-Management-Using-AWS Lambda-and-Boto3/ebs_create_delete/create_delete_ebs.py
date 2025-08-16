import os
import boto3
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

def _now_utc():
    return datetime.now(timezone.utc)

def _parse_volume_ids(raw: str):
    return [v.strip() for v in raw.split(",") if v.strip()]

def create_snapshots(volume_ids, snapshot_prefix):
    created = []
    ts = _now_utc().strftime("%Y-%m-%d_%H-%M-%S")
    for vol_id in volume_ids:
        desc = f"{snapshot_prefix}{vol_id}-{ts}"
        try:
            resp = ec2.create_snapshot(
                VolumeId=vol_id,
                Description=desc,
                TagSpecifications=[
                    {
                        "ResourceType": "snapshot",
                        "Tags": [
                            {"Key": "Name", "Value": desc},
                            {"Key": "CreatedBy", "Value": "Lambda-EBS-Backup"},
                            {"Key": "VolumeId", "Value": vol_id},
                        ],
                    }
                ],
            )
            sid = resp["SnapshotId"]
            created.append(sid)
            print(f"✅ Created snapshot {sid} for {vol_id}")
        except ClientError as e:
            print(f"❌ ERROR creating snapshot for {vol_id}: {e}")
    return created

def list_old_snapshots(volume_ids, older_than_dt, created_by_tag="Lambda-EBS-Backup"):
    to_delete = []
    paginator = ec2.get_paginator("describe_snapshots")
    page_it = paginator.paginate(OwnerIds=["self"])
    vols = set(volume_ids)

    for page in page_it:
        for snap in page.get("Snapshots", []):
            tags = {t["Key"]: t["Value"] for t in snap.get("Tags", [])}
            if tags.get("CreatedBy") != created_by_tag:
                continue
            if tags.get("VolumeId") not in vols:
                continue
            if snap["StartTime"] < older_than_dt:
                to_delete.append(snap["SnapshotId"])
    return to_delete

def delete_snapshots(snapshot_ids):
    deleted = []
    for sid in snapshot_ids:
        try:
            ec2.delete_snapshot(SnapshotId=sid)
            deleted.append(sid)
            print(f"🗑 Deleted snapshot {sid}")
        except ClientError as e:
            print(f"❌ ERROR deleting snapshot {sid}: {e}")
    return deleted

def lambda_handler(event=None, context=None):
    raw_volume_ids = os.environ.get("VOLUME_IDS", "").strip()
    if not raw_volume_ids:
        raise ValueError("VOLUME_IDS env var is required")
    volume_ids = _parse_volume_ids(raw_volume_ids)

    retention_days = int(os.environ.get("RETENTION_DAYS", "30"))
    snapshot_prefix = os.environ.get("SNAPSHOT_PREFIX", "ebs-backup-")

    created = create_snapshots(volume_ids, snapshot_prefix)

    cutoff = _now_utc() - timedelta(days=retention_days)
    old_snaps = list_old_snapshots(volume_ids, cutoff)
    deleted = delete_snapshots(old_snaps)

    result = {
        "created_snapshots": created,
        "deleted_snapshots": deleted,
        "retention_days": retention_days,
        "volumes": volume_ids,
    }
    print("📊 Result:", result)
    return result

# ---------- LOCAL RUN ----------
if __name__ == "__main__":
    # Set env vars manually here for local run
    os.environ["AWS_PROFILE"] = "default"     # requires AWS CLI profile
    os.environ["AWS_REGION"] = "ca-central-1"    # change to your region
    os.environ["VOLUME_IDS"] = "vol-088c61bedfc8811f2"
    os.environ["RETENTION_DAYS"] = "7"
    os.environ["SNAPSHOT_PREFIX"] = "test-backup-"

    # Run like a normal script
    lambda_handler()
