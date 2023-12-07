from azure.storage.blob import BlobServiceClient, BlobClient
import os

def upload_large_file_to_blob(file_path, container_name, blob_name, connection_string):
    try:
        # Create BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get a BlobClient for the specified container and blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Set the chunk size for uploading (4MB in this example)
        chunk_size = 4 * 1024 * 1024  # 4 MB
        
        # Upload the file to Azure Blob Storage using parallel upload
        with open(file_path, "rb") as file:
            blob_client.upload_blob(data=file, blob_type="BlockBlob", length=os.path.getsize(file_path),
                                    max_concurrency=4, max_size=chunk_size)
        
        print(f"File '{os.path.basename(file_path)}' uploaded to '{blob_name}' in container '{container_name}' successfully.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Usage
local_file_path = '/path/to/your/large/file.txt'
your_container_name = 'your-container-name'
your_blob_name = 'your-blob-name'
your_connection_string = 'YOUR_AZURE_STORAGE_CONNECTION_STRING'

upload_large_file_to_blob(local_file_path, your_container_name, your_blob_name, your_connection_string)
