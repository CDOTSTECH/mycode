import os
import zipfile
import tempfile
import shutil
import azure.functions as func

def unzip_blob(trigger: func.InputStream, outputBlob: func.Out[bytes]) -> None:
    try:
        # Create a temporary directory to extract the contents
        temp_dir = tempfile.mkdtemp()

        # Get the name of the uploaded file
        file_name = os.path.basename(trigger.name)

        # Create a temporary file path
        temp_file_path = os.path.join(temp_dir, file_name)

        # Open the temporary file for writing in binary mode
        with open(temp_file_path, 'wb') as file:
            # Stream chunks of the input file and write to the temporary file
            for chunk in trigger:
                file.write(chunk)

        # Unzip the file
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            # Extract all contents to the temporary directory
            zip_ref.extractall(temp_dir)

        # Create a new ZIP file with the extracted contents
        output_zip_path = os.path.join(temp_dir, 'combined.zip')
        with zipfile.ZipFile(output_zip_path, 'w') as output_zip:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add each extracted file to the new ZIP file
                    output_zip.write(file_path, os.path.relpath(file_path, temp_dir))

        # Read the content of the combined ZIP file
        with open(output_zip_path, 'rb') as output_file:
            output_content = output_file.read()

        # Output the content to the outputBlob
        outputBlob.set(output_content)

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

