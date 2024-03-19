# Use the official Python image as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*


# Copy the content of the local src directory to the working directory
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

