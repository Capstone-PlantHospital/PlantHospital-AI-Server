import boto3
import os
from datetime import datetime


def upload_file(filename, BUCKET):
    result_file_name = filename.split('.')[0]
    result_file_path = "./runs/detect/exp/{}.jpg".format(result_file_name)
    unique_file_name = result_file_name + '_' + datetime.now().strftime("%Y%m%d%H%M%S.%f")
    img_url = ""

    s3 = s3_connection()
    if s3_put_object(s3, BUCKET, result_file_path, unique_file_name + '.jpg'):
        img_url = s3_get_image_url(s3, BUCKET, unique_file_name)

    return img_url


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


def s3_get_image_url(s3, BUCKET, filename):
    location = s3.get_bucket_location(Bucket=BUCKET)["LocationConstraint"]

    return f"https://planthospital.s3.{location}.amazonaws.com/{filename}.jpg"
