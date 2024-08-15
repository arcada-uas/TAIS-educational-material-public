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

# Expose the necessary ports
EXPOSE 8061

# Command to run the server
CMD ["python3", "data_service_server.py"]
