"""Extract data from S3 Buckets."""

# pylint: skip-file

import os
from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client
import pandas as pd


def get_bucket_names(s3_client: client) -> list[str]:
    """Returns a list pf S3 bucket names."""

    buckets = s3_client.list_buckets()["Buckets"]

    return [b["Name"] for b in buckets]


def get_object_names_from_bucket(s3_client: client, bucket_name: str) -> list[str]:
    """Returns a list pf S3 bucket names."""

    objects = s3_client.list_objects(Bucket=bucket_name)["Contents"]

    return [o["Key"] for o in objects]


def combine_csv_files(path: str):
    """Combines csv files and deletes once we're done using them. """
    list_of_files = os.listdir(path)
    combined_data = pd.DataFrame()

    for file in list_of_files:
        if file.endswith(".csv"):
            file_path = os.path.join(path, file)
            df_temp = pd.read_csv(file_path)
            combined_data = pd.concat(
                [combined_data, df_temp], ignore_index=True)
            os.remove(file_path)

    return combined_data


if __name__ == "__main__":

    load_dotenv()  # Reads variables from .env into the environment

    s3 = client("s3", aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    items = get_object_names_from_bucket(s3, ENV["S3_BUCKET_NAME"])

    for i in items:
        if i.endswith(".json") and i.startswith("lmnh"):
            s3.download_file(ENV["S3_BUCKET_NAME"],
                             i, f"data/{i}")
        elif i.endswith(".csv") and i.startswith("lmnh"):
            s3.download_file(ENV["S3_BUCKET_NAME"],
                             i, f"data/{i}")

    FILE_PATH = "data/"
    df = combine_csv_files(FILE_PATH)
    df.to_csv(os.path.join(FILE_PATH, "lmnh_combined_hist.csv"), index=False)

    s3.close()
