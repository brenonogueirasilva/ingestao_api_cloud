from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import pandas as pd
import logging
from classes.all import decorator_try_except
from logger import trace_id

class BigQuery:
    """
    A class for interacting with Google BigQuery using the Python client library.
    """
    def __init__(self):
        self.client = bigquery.Client()