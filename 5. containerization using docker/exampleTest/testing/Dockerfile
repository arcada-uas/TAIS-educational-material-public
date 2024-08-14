FROM ubuntu:22.04

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install required packages
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    pip3 install --upgrade pip

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports used by Flask and gRPC
EXPOSE 8062 8061

# Command to run both the Flask app and the gRPC server
CMD ["python3", "test_service_server.py"]
