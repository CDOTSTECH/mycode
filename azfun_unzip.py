import os
import tempfile
import zipfile
import azure.functions as func

def unzip_blob(trigger: func.BlobTrigger, outputblob: func.Out[str]) -> None:
    # Get the blob name
    blob_name = os.path.basename(trigger.name)

    # Temporary directory to extract files
    temp_dir = tempfile.mkdtemp()

    # Path to save the extracted files
    extract_path = os.path.join(temp_dir, blob_name)

    # Connect to Azure Blob Storage
    blob_service_client = trigger.bindings[0].blob_service_client

    # Get the blob
    blob_client = blob_service_client.get_blob_client(container=trigger.container_name, blob=trigger.name)
    blob_properties = blob_client.get_blob_properties()

    try:
        # Download the blob into a temporary file
        download_path = os.path.join(temp_dir, blob_name)
        with open(download_path, "wb") as file:
            download_stream = blob_client.download_blob()
            file.write(download_stream.readall())

        # Unzip the file
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # List extracted files for demonstration purposes
        extracted_files = os.listdir(extract_path)
        for file_name in extracted_files:
            file_path = os.path.join(extract_path, file_name)
            with open(file_path, 'rb') as file:
                outputblob.set(file.read())
                # Here, you can process the extracted files as needed (e.g., upload to another location)

        # Clean up temporary directory
        os.remove(download_path)
        os.rmdir(temp_dir)
    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")

def main(trigger: func.BlobTrigger, outputblob: func.Out[str]) -> None:
    unzip_blob(trigger, outputblob)
