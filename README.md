# Extractify-Automatic-License-Plate-Detector API
The License Plate Recognition API is a service that allows you to retrieve license plate information from an image. By sending an image containing a license plate, the API performs license plate recognition and returns a JSON response containing the license plate number.

# Getting Started
## Install all required packages & libraries
`pip install -r requirements.txt`
## Install OpenMP
### On Linux (Ubuntu, Debian, etc.):
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

## Configure Makefile
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

## Make Darknet
The `make` command builds darknet so that the darknet executable file can be used to run detectors.

Make sure you are in the darknet directory then run this command: `make`


# Automatic License Plate Detector
In the main directory, there are two python files:

**ALPD.py:** Detects the license plate in an image and crops out the license plate from an image. It then runs OCR on the detected license plate, and returns a string containing the plate number, the confidence score of the OCR, and the top left and bottom right coordinates of the cropped area containing the license plate.

**ALPD_api.py:** The automatic plate detector as an API.
