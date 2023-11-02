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