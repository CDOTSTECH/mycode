import zipfile

def unzip_large_file(zip_file_path, extract_path, buffer_size=8192):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            with zip_ref.open(file_info, 'r') as file_in_zip:
                with open(f"{extract_path}/{file_info.filename}", 'wb') as output_file:
                    while True:
                        buffer = file_in_zip.read(buffer_size)
                        if not buffer:
                            break
                        output_file.write(buffer)

# Example usage
zip_file_path = 'path/to/your/large_file.zip'
extract_path = 'path/to/extract'
unzip_large_file(zip_file_path, extract_path)
