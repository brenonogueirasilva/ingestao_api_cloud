from classes.api_orquestrator import ApiOrquestrator
import google.cloud.logging
import os
import logging
from logger import trace_id

def main(request):

    folder_name = request.args.get('folder')
    local = request.args.get('local')

    if local == '1':
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  '../apt-theme-402300-32506a51a70d.json'

    client = google.cloud.logging.Client()
    client.setup_logging()

    bucket_name = 'brasil_api'
    logging.info('Starting Object Api Orquestrator' , extra={"json_fields": trace_id})
    orquestrador = ApiOrquestrator(
        endpoint= "ibge/municipios/v1/",
        query_parameters =  { "providers" : "dados-abertos-br,gov,wikipedia"},
        path_parameters = ['AL' , 'RR'],
        download_folder= folder_name,
        bucket= bucket_name
    )
    logging.info('Executings requests to API', extra={"json_fields": trace_id})
    orquestrador.execute_requests_envelope_save_file()
    logging.info('Opening Json Files from Cloud Storage and Saving in Big Query' , extra={"json_fields": trace_id})
    orquestrador.json_files_to_big_query(bucket_name, folder_name)
    return ('Script executed with sucess')