# Extractify-Automatic-License-Plate-Recognition API
The Automatic License Plate Recognition (ALPR) API is a service that performs license plate recognition on an uploaded image and returns the result in JSON format. By sending an image containing a license plate, the API runs the ALPR algorithm and provides the recognized license plate information.

# Usage
To use the ALPR API, you need to send an HTTP POST request to the specified endpoint along with the image file in the request payload. The API will save the uploaded image, process it using the ALPR algorithm, and return a JSON response containing the recognized license plate information.

**Endpoint**
`POST /api/ALPR`

**Request**

- Method: `POST`
- Content-Type: `multipart/form-data`

_Request Parameters_

- `file`: The image file containing the license plate. Include it as a form-data field in the request payload.

**Response**

The API will respond with a JSON object containing the license plate number, the confidence of the OCR, and the top left and bottom right coordinates containing the license plate.

_Response Example_
`["BXG7C59",90,[329,196],[451,243]]`

# Setup and Installation

To set up the ALPR API locally, follow these steps:

## 1. Install python

**Note: this project requires Python 3.7, 3.8, 3.9, or 3.10 to run**

Check if python is already installed: `python --version`

## 2. Clone the repository

`https://github.com/JerryHamm/Extractify-Automatic-License-Plate-Recognition.git`

## 3. Install all required packages & libraries
`pip install -r requirements.txt`

## 4. Install OpenMP
### On Linux (Ubuntu, Debian, etc...):
Install GCC and OpenMP.

`sudo apt install build-essential`

`sudo apt install libomp-dev`

verify the installation by checking the version of GCC.

`gcc --version`

### On macOs:
Install Homebrew (if not already installed).

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Install LLVM (which includes Clang and OpenMP).

`brew install llvm`

Verify the installation by checking the version of Clang.

`clang --version`

### On Windows:
For Windows, you can use the MinGW-w64 distribution, which includes GCC with OpenMP support. Here's how to install OpenMP using MinGW-w64:

1. Download the MinGW-w64 installer from the official website: https://mingw-w64.org/doku.php/download.

2. Run the installer and follow the installation instructions. **_During the installation process, make sure to select the "OpenMP" component._**

3. Add the MinGW-w64 binaries to your system's PATH environment variable. The exact steps to do this depend on your version of Windows. You can find instructions online specific to your version of Windows.

## 5. Configure Makefile
Enter the darknet directory: `cd darknet`

Open and edit the Makefile: `nano Makefile`

### For GPU use
set `GPU=1` and `CUDNN=1` to speedup on GPU

set `CUDNN_HALF=1` to further speedup 3 x times (Mixed-precision on Tensor Core).

set `OPENCV=1` Enabling OpenCV is necessary if you want to utilize the GPU for accelerating computer vision tasks in Darknet.

**_Note: if you enable opencv you must make sure opencv is installed by running `pkg-config --modversion opencv` (for Linux and macOS). If opencv is not installed you have to install it_**

set `LIBSO=1` to enable the creation of a dynamic library so that pre-compiled code can be dynamically linked and loaded at runtime by other programs.

### For CPU only
set `AVX=1` and `OPENMP=1` to speedup on CPU (if errors occur then set AVX=0).

set `LIBSO=1` to enable the creation of a dynamic library so that pre-compiled code can be dynamically linked and loaded at runtime by other programs.

## 6. Make Darknet
The `make` command builds darknet so that the darknet executable file can be used to run detectors.

Make sure you are in the darknet directory then run this command: `make`

# Technologies Used

- Darknet: Open-source neural network framework written in C and CUDA. It is used for training and implementing deep neural networks, including object detection models like YOLO (You Only Look Once).

- YOLOv4: YOLOv4 (You Only Look Once version 4 a state-of-the-art real-time object detection model). The algorithm employs the YOLOv4-tiny variant for license plate detection. The algorithm uses Darknet for license plate detection.

- PaddleOCR: PaddleOCR is an open-source optical character recognition (OCR) library based on PaddlePaddle, a deep learning platform. It is used for text recognition on cropped license plate images.

- OpenCV: Open Source Computer Vision Library

- Python: The algorithm is implemented in the Python programming language, which provides a wide range of libraries and tools.

- FastAPI: a high-performance web framework for building APIs with Python. With FastAPI, you can create an API that exposes the ALPR algorithm's functionality, allowing users to send images for license plate recognition.

- PIL (Python Imaging Library): PIL is a Python library for image processing. It provides functions for image loading, manipulation, enhancement, and filtering. The algorithm utilizes PIL for image preprocessing.

- Computer Vision: The algorithm leverages computer vision techniques to process images and extract relevant information from license plates.
