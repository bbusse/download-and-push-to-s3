#!/usr/bin/env python3
import os
import requests
import boto3
from botocore.exceptions import ClientError

def download_and_upload_file():
    """
    Downloads a file from URL in env var and uploads it to S3 bucket and path from env vars
    """
    # Get URL, bucket name, and file path from environment variables
    file_url = os.getenv('FILE_URL')
    bucket_name = os.getenv('S3_BUCKET')
    s3_file_path = os.getenv('S3_FILE_PATH')

    # Check if environment variables are set
    if not file_url:
        raise ValueError("FILE_URL environment variable not set")
    if not bucket_name:
        raise ValueError("S3_BUCKET environment variable not set")
    if not s3_file_path:
        raise ValueError("S3_FILE_PATH environment variable not set")

    try:
        # Download the file
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes

        # Save file temporarily
        temp_filename = 'temp_downloaded_file'
        with open(temp_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        # Initialize S3 client
        s3_client = boto3.client('s3')

        # Upload file to S3
        try:
            s3_client.upload_file(
                temp_filename,
                bucket_name,
                s3_file_path
            )
            print(f"Successfully uploaded {s3_file_path} to {bucket_name}")

        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            raise

        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    try:
        download_and_upload_file()
    except Exception as e:
        print(f"Failed to complete operation: {e}")
