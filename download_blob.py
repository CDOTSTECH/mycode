import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_str = os.environ["AzureWebJobsStorage"]
    container_name = "your-container-name"
    blob_name = "your-blob-name"
    download_path = "downloaded-file-path"

    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        logging.info(f"Blob '{blob_name}' downloaded to '{download_path}'")
        return func.HttpResponse("Blob downloaded successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Error downloading blob '{blob_name}': {str(e)}")
        return func.HttpResponse("Error downloading blob.", status_code=500)
