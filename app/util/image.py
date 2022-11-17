import boto3
import os


def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
    except Exception as e:
        print(e)
    else:
        return s3


def s3_put_object(s3, bucket, filepath, access_key):
    try:
        s3.upload_file(
            Filename=filepath,
            Bucket=bucket,
            Key=access_key,
            ExtraArgs={"ContentType": "image/jpg", "ACL": "public-read"},
        )
    except Exception as e:
        print(e)
        return False

    return True


def s3_get_image_url(s3, filename):
    location = s3.get_bucket_location(Bucket="planthospital")["LocationConstraint"]

    return f"https://planthospital.s3.{location}.amazonaws.com/{filename}.jpg"
