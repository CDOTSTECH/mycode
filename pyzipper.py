import pyzipper

# Extract files from a password-protected ZIP file
def extract_zip_with_password(zip_filename, password, extract_to):
    with pyzipper.AESZipFile(zip_filename, 'r') as zipf:
        zipf.setpassword(password.encode('utf-8'))
        zipf.extractall(path=extract_to)

# Example usage
extract_zip_with_password('protected.zip', 'your_password', 'extracted_files')

---------------
import gzip
import shutil

def extract_gzip(gzip_filename, extract_to):
    with gzip.open(gzip_filename, 'rb') as f_in:
        with open(extract_to, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

extract_gzip('large_file.gz', 'extracted_file')
