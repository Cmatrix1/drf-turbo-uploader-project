# drf-turbo-uploader

drf-turbo-uploader is an open source project that provides a Django-based solution for uploading large files in chunks. This project is designed to handle file uploads quickly and efficiently, allowing async clients to send files without any order.

## Features

- Upload large files in chunks
- Handle file uploads quickly and efficiently
- Support for async clients
- Easy integration with Django

## Description 📝
Our project has three endpoints for uploading files in chunks: 

1. Create File: POST endpoint for creating the file object and receiving a UUID to resume uploading. 🆕
2. Upload Chunks: POST endpoint for uploading file chunks. You can cut your file into as many chunks as you want and specify the size. 📤
3. Complete Upload: when all the file chunks have been uploaded, you should send a GET request with the file ID and indicate that the upload is finished. In response, you will receive the file information on the server. 🎉

I hope this helps! Let me know if you have any other questions.


## Python Client
Here's a sample Python client for this Project that shows you how to upload a file in chunks. 🚀
```python

import requests
import threading

# Set the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Set the name of the file to upload
file_name = "big_file.zip"

# Create a file object on the server
def create_file_object(filename):
    data = {"filename": filename}
    response = requests.post(f"{BASE_URL}/upload/", data=data)
    return response

# Upload a chunk of the file to the server
def upload_chunk(file_id, order, chunk):
    data = {"order": order}
    response = requests.post(f"{BASE_URL}/upload/{file_id}", data=data, files={'file': chunk})
    return response

# Tell the server that the upload is complete
def complete_upload(file_id):
    response = requests.get(f"{BASE_URL}/upload/complete/{file_id}")
    return response

# Create a file object on the server and get the file ID
file_id = create_file_object(file_name).json()["id"]

# Open the file to upload
with open(file_name, "rb") as file:
    # Define a function to read chunks of the file
    read_method = lambda: file.read(1_000_000)
    threads = []
    # Upload each chunk of the file in a separate thread
    for order, chunk in enumerate(iter(read_method, b'')):
        t = threading.Thread(target=upload_chunk, args=(file_id, order, chunk))
        t.start()
        threads.append(t)
    
    # Wait for all threads to finish
    for t in threads:
        t.join()

# Tell the server that the upload is complete and get the file URL
complete = complete_upload(file_id)
file_url = BASE_URL + complete.json()["url"]

# Print the URL of the uploaded file
print("[+] Upload Complete:", file_url)
```
