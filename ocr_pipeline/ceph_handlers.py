from minio import Minio
from minio.error import S3Error
from settings import settings

# Configuration
endpoint = settings.get_environment_variable("MINIO_ENDPOINT")
access_key = settings.get_environment_variable("MINIO_ACCESS_KEY")
secret_key = settings.get_environment_variable("MINIO_SECRET_KEY")
secure = settings.get_environment_variable("MINIO_SECURE")

# Initialize MinIO client
client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)


# Upload a file
def upload_file(bucket_name, object_name, file_path):
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

        client.fput_object(bucket_name, object_name, file_path)
        print(
            f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'."
        )
    except S3Error as err:
        print(f"S3 Error: {err}")
    except Exception as e:
        print(f"Error: {e}")


# Download a file
def download_file(bucket_name, object_name, download_path):
    try:
        client.fget_object(bucket_name, object_name, download_path)
        print(
            f"File '{object_name}' from bucket '{bucket_name}' downloaded to '{download_path}'."
        )
    except S3Error as err:
        print(f"S3 Error: {err}")
    except Exception as e:
        print(f"Error: {e}")







