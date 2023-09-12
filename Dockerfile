# Use the official Python image from the DockerHub
FROM python:3.10-slim

# Set the working directory in docker
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y locales && \
    sed -i -e 's/# da_DK.UTF-8 UTF-8/da_DK.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=da_DK.UTF-8

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies inside virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local directory to the working directory
COPY . .

# Specify the command to run on container start and --workers, --host and --port 
CMD ["./docker-server.sh", "server-docker", "--workers=3"]

# Expose the port the app runs on
EXPOSE 5555
