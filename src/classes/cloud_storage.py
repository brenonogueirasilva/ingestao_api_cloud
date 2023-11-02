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