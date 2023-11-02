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

    @decorator_try_except
    def select(self, sql_query: str) ->pd.DataFrame:
        """
        Execute a SQL query in BigQuery and return the results as a DataFrame.
        Args:
            sql_query (str): The SQL query to be executed.

        Returns:
            pandas.DataFrame: A DataFrame containing the query results.
        """
        query_job = self.client.query(sql_query) 
        dataframe = query_job.to_dataframe()
        return dataframe