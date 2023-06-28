# Use a base image with Python support
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install build-essential, libomp-dev, libgl1-mesa-glx, libglib2.0-0
RUN apt-get update && apt-get install -y build-essential libomp-dev libgl1-mesa-glx libglib2.0-0

# Copy the necessary files to the container
COPY requirements.txt .
COPY ALPR_api.py .
COPY ALPR.py .
COPY darknet/ darknet/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Change working directory to darknet
WORKDIR /app/darknet

# Compile darknet using make
RUN make

# Return to the app directory
WORKDIR /app

# Expose the API port
EXPOSE 8000

# Set the entrypoint command to start the API
CMD ["uvicorn", "ALPR_api:app", "--host", "0.0.0.0", "--port", "8000"]

