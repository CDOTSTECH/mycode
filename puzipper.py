import pyzipper

# Extract files from a password-protected ZIP file
def extract_zip_with_password(zip_filename, password, extract_to):
    with pyzipper.AESZipFile(zip_filename, 'r') as zipf:
        zipf.setpassword(password.encode('utf-8'))
        zipf.extractall(path=extract_to)

# Example usage
extract_zip_with_password('protected.zip', 'your_password', 'extracted_files')
