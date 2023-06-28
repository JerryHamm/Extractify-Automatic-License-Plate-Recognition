# Extractify-Automatic-License-Plate-Recognition API
The Automatic License Plate Recognition (ALPR) API is a service that performs license plate recognition on an uploaded image and returns the result in JSON format. By sending an image containing a license plate, the API runs the ALPR algorithm and provides the recognized license plate information.

## Features

- License plate detection using Darknet
- License plate number extraction using PaddleOCR
- API endpoint to receive an image and return the license plate number
- Dockerized for easy deployment and portability

## Requirements

- Docker

## Usage

1. Clone the repository:
   ```shell
    git clone https://github.com/JerryHamm/Extractify-Automatic-License-Plate-Recognition.git
    cd Extractify-Automatic-License-Plate-Recognition

2. Build the Docker image:
   ```shell
   docker build -t alpr-api .

3. Run the Docker container:
   ```shell
   docker run -d -p 8000:8000 alpr-api

4. The ALPR API is now accessible at 'http://localhost:8000'. You can send an image containing a license plate to the API and retrieve the license plate number.


# API Documentation
### Endpoint
POST `/api/ALPR`

### Request

- Method: `POST`
- Content-Type: `multipart/form-data`

### Request Parameters

- `file`: The image file containing the license plate. Include it as a form-data field in the request payload.

### Response

The API will respond with a JSON object containing the license plate number, the confidence of the OCR, and the top left and bottom right coordinates containing the license plate.

### Response Example
     
    ["BXG7C59",90,[329,196],[451,243]]


# Customization
You can customize the ALPR API by modifying the source code and Dockerfile to suit your specific requirements.

