from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
import requests
import pandas as pd
import json
import logging
from classes.all import decorator_try_except
from logger import trace_id


class CloudStorage:
    """
    A class for interacting with Google Cloud Storage, including operations such as creating buckets, uploading and downloading objects,
    handling JSON, and more.
    """
    def __init__(self):
        self.storage_client = storage.Client()
    
    @decorator_try_except
    def create_bucket(self, bucket_name: str, location : str ='us-central1'):
        """
        Creates a new bucket in Google Cloud Storage.
        Args:
            bucket_name (str): The name of the bucket to be created.
            storage_class (str, optional): The storage class of the bucket. Default is 'STANDARD'.
            location (str, optional): The location of the bucket. Default is 'us-central1'.
        """ 
        bucket = self.storage_client.create_bucket(bucket_name, location=location)     
        return f'Bucket {bucket.name} successfully created.'
    
    @decorator_try_except
    def list_buckets(self):
        """
        Lists all buckets in the Google Cloud project.

        Returns:
            List[str]: A list of bucket names.
        """
        buckets = self.storage_client.list_buckets()
        list_buckets = []
        for item in buckets:
            list_buckets.append(item.name)
        return list_buckets
    
    @decorator_try_except
    def upload_object(self, bucket_name: str, name_file: str, source_file_name: str, folder: str=None):
        """
        Uploads an object to a bucket in Google Cloud Storage.
        Args:
            bucket_name (str): The name of the target bucket.
            name_file (str): The name of the file in the bucket.
            source_file_name (str): The name of the local source file.
            folder (str, optional): The folder in the bucket where the file will be stored.
        """
        if folder is not None:
            name_file = f"{folder}/{name_file}"
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        blob.upload_from_filename(source_file_name)
        logging.info('Object Uploaded with Sucess' , extra={"json_fields": trace_id})