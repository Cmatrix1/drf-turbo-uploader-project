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
