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

    def generate_list_query__path_parameters(self) -> list:
        """
        Generate a list of dictionaries with combined query and path parameters.

        Returns:
            list: A list of dictionaries, each containing 'path' and 'query_parameter' keys.
        """
        query_parameter = self.query_parameters.copy()
        for key, value in query_parameter.items():
            query_parameter[key] = [value] 
        df_parameters = pd.DataFrame(query_parameter)
        for column in df_parameters.columns:
            df_parameters = df_parameters.explode(column)
        ls_query_parameters = df_parameters.to_dict(orient='records')
        ls_parameters = []            
        for path in self.path_parameters:
            for query in ls_query_parameters:
                ls_parameters.append( {'path' : path, 'query_parameter' : query} )
        return ls_parameters
    
    def execute_requests_save_file(self):
        """
        Execute API requests, save responses to JSON files.
        """
        ls_query_path_parameters = self.generate_list_query__path_parameters()
        for dict_query_parameters in ls_query_path_parameters:
            obj_brasil_api = BrasilApi(
                endpoint= self.endpoint,
                query_parameter= dict_query_parameters['query_parameter'],
                path_parameter= dict_query_parameters['path'] 
            )
            response = obj_brasil_api.request_get()
            name_file = obj_brasil_api.generate_name_file()
            self.storage_object.request_to_json_file(self.bucket, response, name_file, self.download_folder)

    def execute_requests_envelope_save_file(self):
        """
        Execute API requests, envelope responses, and save to JSON files.
        """
        ls_query_path_parameters = self.generate_list_query__path_parameters()
        for dict_query_parameters in ls_query_path_parameters:
            obj_brasil_api = BrasilApi(
                endpoint= self.endpoint,
                query_parameter= dict_query_parameters['query_parameter'],
                path_parameter= dict_query_parameters['path'] 
            )
            response = obj_brasil_api.request_get()
            envelope = obj_brasil_api.generate_envelope()
            name_file = obj_brasil_api.generate_name_file()
            json_payload ={'trace_id' : trace_id_value, 'content' : envelope['envelope']}
            print(json_payload)
            logging.info('Executing Requests with envelope and save file in cloud storage', extra={"json_fields": json_payload})
            self.storage_object.request_to_json_envelope_file(self.bucket, response, name_file, envelope, self.download_folder)

    def json_files_to_big_query(self, bucket_name: str, folder_name: str):
        '''
        Open Json files from CloudStorage and save into big query
        '''
        for item in self.storage_object.list_objects_buckets(bucket_name, folder_name):
            df = self.storage_object.json_envelope_to_dataframe(bucket_name, item)
            logging.info(f'Opening json file: {folder_name} with envelope and save file in bigquery' , extra={"json_fields": trace_id})
            self.big_query.insert_dataframe_append('brasil_api', 'municipios', df)