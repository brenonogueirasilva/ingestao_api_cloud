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

    @decorator_try_except
    def request_to_json_file(self, bucket_name: str, object_request: requests.Response, name_file: str, folder: str = None):
        """
        Uploads a JSON object from a request response into a json file in the bucket.
        Args:
            bucket_name (str): The name of the target bucket.
            object_request (requests.Response): The response from the request containing the JSON.
            name_file (str): The name of the file in the bucket.
            folder (str, optional): The folder in the bucket where the file will be stored.
        """
        if folder is not None:
            name_file = f"{folder}/{name_file}"
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        json_string = json.dumps(object_request.json())
        json_bytes = json_string.encode('utf-8')
        blob.upload_from_string(json_bytes, content_type='application/json') 
        logging.info('INFO Request Object uploaded with sucess' , extra={"json_fields": trace_id})

    @decorator_try_except
    def request_to_json_envelope_file(self, bucket_name, object_request: requests.Response, name_file: str, envelope: dict, folder = None):
        """
        Uploads a JSON object with an envelope from a request response into a file in the bucket.
        Args:
            bucket_name (str): The name of the target bucket.
            object_request (requests.Response): The response from the request containing the JSON.
            name_file (str): The name of the file in the bucket.
            envelope: The envelope to be included in the JSON file.
            folder (str, optional): The folder in the bucket where the file will be stored.
        """
        if folder is not None:
            name_file = f"{folder}/{name_file}"
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        json_content = {}
        json_content['envelope'] = envelope['envelope']
        json_content['content'] = object_request.json()
        json_string = json.dumps(json_content)
        json_bytes = json_string.encode('utf-8')
        blob.upload_from_string(json_bytes, content_type='application/json') 
        logging.info('INFO Request Object with envelope uploaded with sucess' , extra={"json_fields": trace_id})


    @decorator_try_except
    def list_objects_buckets(self, bucket_name: str, folder = None) -> str:
        """
        Lists all objects in a specified bucket.
        Args:
            bucket_name (str): The name of the target bucket.
        """
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        list_files = []
        for item in blobs:
            list_files.append(item.name)
        if folder is not None:
            list_files = list(filter(lambda item : folder in item, list_files))
        return list_files
    
    @decorator_try_except
    def delete_file(self, bucket_name: str, name_file: str):
        """
        Deletes a file from a bucket.
        Args:
            bucket_name (str): The name of the target bucket.
            name_file (str): The name of the file to be deleted.
        """
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        blob.delete()
        logging.info("INFO File {} deleted.".format(blob.name) , extra={"json_fields": trace_id})

    
    @decorator_try_except
    def delete_bucket(self, bucket_name: str):
        """
        Deletes a bucket and all its contents.
        Args:
            bucket_name (str): The name of the bucket to be deleted.
        """
        bucket = self.storage_client.get_bucket(bucket_name)
        bucket.delete()
        logging.info("INFO Bucket {} deleted.".format(bucket.name) , extra={"json_fields": trace_id})


    @decorator_try_except
    def download_object(self, bucket_name: str, file_name: str, output_file_name: str):
        """
        Downloads an object from a bucket to a local file.
        Args:
            bucket_name (str): The name of the target bucket.
            file_name (str): The name of the object in the bucket.
            output_file_name (str): The name of the local output file.
        """
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        blob.download_to_filename(output_file_name)

    @decorator_try_except
    def json_to_dataframe(self, bucket_name: str, name_file: str, folder: str = None) -> pd.DataFrame:
        """
        Converts a JSON object in a file in the bucket to a Pandas DataFrame.
        Args:
            bucket_name (str): The name of the target bucket.
            name_file (str): The name of the JSON file in the bucket.
            folder (str, optional): The folder in the bucket where the file is stored.

        Returns:
            pd.DataFrame: A Pandas DataFrame representing the JSON data.
        """
        if folder is not None:
                name_file = f"{folder}/{name_file}"
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        json_string = blob.download_as_text()
        data_frame = pd.read_json(json_string)
        return data_frame
    
    @decorator_try_except
    def json_envelope_to_dataframe(self, bucket_name: str, name_file: str, folder: str = None) -> pd.DataFrame:
        """
        Converts a JSON object with an envelope in a file in the bucket to a Pandas DataFrame.
        Args:
            bucket_name (str): The name of the target bucket.
            name_file (str): The name of the JSON file in the bucket.
            folder (str, optional): The folder in the bucket where the file is stored.
        """
        if folder is not None:
                name_file = f"{folder}/{name_file}"
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(name_file)
        json_dict = json.loads(blob.download_as_text())
        data_frame = pd.DataFrame(json_dict['content'])
        for key, value in json_dict['envelope'].items():
            data_frame[key] = value 
        return data_frame