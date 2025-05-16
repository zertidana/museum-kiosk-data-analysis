"""Connects the kiosk data to the database."""

# pylint: skip-file

import logging
import argparse
import os
from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client
import pandas as pd


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)


def parse_args():
    """CLI commands."""
    parser = argparse.ArgumentParser(description="Upload data to AWS and DB.")

    parser.add_argument('--bucket', type=str, default=os.getenv('S3_BUCKET_NAME', 'default-bucket'),
                        help='Name of the AWS S3 bucket.')
    parser.add_argument('--rows', type=str, default=str(os.getenv('ROW_LIMIT', '1000')),
                        help='Number of rows to upload.')
    parser.add_argument('--logs', action='store_true',
                        help='If set, logs will be written to a file instead of the terminal.')

    return parser.parse_args()


def get_bucket_names(s3_client: client) -> list[str]:
    """Returns a list pf S3 bucket names."""

    buckets = s3_client.list_buckets()["Buckets"]
    bucket_names = [b["Name"] for b in buckets]

    if bucket_names == []:
        logging.warning("No buckets found.")
        return []

    logging.info(
        "Found %s s3 buckets.", len(bucket_names))
    return bucket_names


def get_object_names_from_bucket(s3_client: client, bucket_name: str) -> list[str]:
    """Returns a list of S3 object names from bucket."""

    objects = s3_client.list_objects(Bucket=bucket_name)["Contents"]
    keys = [o["Key"] for o in objects]

    if keys == []:
        logging.warning("No objects found in bucket %s.", bucket_name)
        return []

    logging.info("Found %s objects in bucket %s.", len(keys), bucket_name)
    return keys


def combine_csv_files(path: str):
    """Combines csv files and deletes once we're done using them. """
    list_of_files = os.listdir(path)
    combined_data = pd.DataFrame()

    for file in list_of_files:
        if file.endswith(".csv"):
            logging.info('Found a csv file.')
            file_path = os.path.join(path, file)
            df_temp = pd.read_csv(file_path)
            combined_data = pd.concat(
                [combined_data, df_temp], ignore_index=True)
            os.remove(file_path)

    return combined_data


if __name__ == "__main__":
    args = parse_args()

    load_dotenv()
    CSV_PATH = "data/"

    s3 = client("s3", aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    items = get_object_names_from_bucket(s3, args.bucket)

    for i in items:
        if i.endswith(".json") and i.startswith("lmnh"):
            logging.info('Adding JSON files...')
            s3.download_file(ENV["S3_BUCKET_NAME"],
                             i, f"{CSV_PATH}/{i}")
        elif i.endswith(".csv") and i.startswith("lmnh"):
            logging.info('Adding CSV files...')
            s3.download_file(ENV["S3_BUCKET_NAME"],
                             i, f"{CSV_PATH}/{i}")

    logging.info('Combining CSV files...')
    df = combine_csv_files(CSV_PATH)
    df.to_csv(os.path.join(CSV_PATH, "lmnh_combined_hist.csv"), index=False)

    s3.close()
