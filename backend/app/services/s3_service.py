from pathlib import Path
import boto3

def download_env_file():
    """
    Downloads the .env file from the S3 bucket to the home directory.
    """
    try:
        home_dir = Path(__file__).resolve(strict=True).parents[2]
        BUCKET_NAME = "leclens"
        s3 = boto3.client('s3')
        s3.download_file(BUCKET_NAME, '.env', f"{home_dir}/.env")
        print(f".env file downloaded successfully to {home_dir}/.env")
    except Exception as e:
        print(f"Error downloading .env file: {e}")