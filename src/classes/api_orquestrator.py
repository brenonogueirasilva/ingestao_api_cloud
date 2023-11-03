import pandas as pd

from classes.brasil_api import BrasilApi
from classes.cloud_storage import CloudStorage
from classes.bigquery import BigQuery
import logging
from logger import trace_id_value
from logger import trace_id

class ApiOrquestrator:
    """
    An API orchestrator class for handling requests, processing responses, and saving data for multiples requests, passing lists on paremeters 
    Args:
        endpoint (str): The API endpoint URL.
        query_parameters (dict): Dictionary of query parameters for API requests.
        path_parameters (list): List of path parameters for API requests (default is [None]).
        token (str): Authentication token for API requests (default is None).
        download_folder (str, optional): The folder where downloaded files will be saved in CloudStorage.
    """
    def __init__(self, endpoint: str, query_parameters: dict, bucket: str, path_parameters: list = [None] ,  token: str = None, download_folder: str = None, trace_id: int = None):
        self.endpoint = endpoint
        self.query_parameters = query_parameters
        self.path_parameters = path_parameters
        self.token = token
        self.bucket = bucket
        self.download_folder = download_folder
        self.storage_object = CloudStorage()
        self.big_query = BigQuery()