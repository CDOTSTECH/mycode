import snappy

def compress_large_file(input_filename, output_filename, chunk_size=1024*1024):
    with open(input_filename, 'rb') as input_file:
        with open(output_filename, 'wb') as output_file:
            while True:
                chunk = input_file.read(chunk_size)
                if not chunk:
                    break

                compressed_chunk = snappy.compress(chunk)
                output_file.write(compressed_chunk)
