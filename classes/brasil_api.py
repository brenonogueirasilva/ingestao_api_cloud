import requests
import pandas as pd
import logging
from logger import trace_id

class BrasilApi:
    '''
    Class for interacting with the BrasilAPI (https://brasilapi.com.br/).

    Parameters:
        - endpoint (str): The specific API endpoint you want to access.
        - query_parameter (str): Query parameter for the request in string format.
        - path_parameter (dict, optional): Path parameter for the request in a dictionary.
        - token (str, optional): An authentication token (if applicable) to access restricted resources.
    '''
    def __init__(self, endpoint : str,  query_parameter : dict, path_parameter: str, token: str = None):
        self.url = "https://brasilapi.com.br/api/"
        self.endpoint = endpoint 
        self.query_parameter = query_parameter
        self.path_parameter = path_parameter
        self.token = token
    
    def request_get(self) -> requests.Response:
        '''
        Makes a request to the BrasilAPI with the specified parameters.

        Returns:
            requests.Response: The response object of the request.
        '''
        if self.token is not None:
            header = {
                "chave-api-dados" : self.token
            }
        else:
            header = None

        if self.path_parameter is None:
            complete_url = self.url + self.endpoint
        else:
            complete_url = self.url + self.endpoint + self.path_parameter

        try:
            response = requests.get(url= complete_url, headers= header, params= self.query_parameter)
            if response.status_code == 200:
                return response
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error("ERROR There was an error in your solicitation" , extra={"json_fields": trace_id})
            logging.error("ERROR" + error , extra={"json_fields": trace_id})

    def generate_name_file(self) -> str:
        '''
        Generates a file name based on the query and path parameters specified.

        Returns:
            str: The generated file name.
        '''
        name_file = self.endpoint.split('/')
        name_file = list(filter(lambda item : 'v' not in item and len(item) > 1, name_file))
        name_file = "_".join(name_file)
        if self.path_parameter is not None:
            name_file = f"{name_file}_path({self.path_parameter})" 
        for key, value in self.query_parameter.items():
            name_file = f"{name_file}_{key}({value}).json" 
        return name_file