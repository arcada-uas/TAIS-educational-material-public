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

# Expose the port used by the Flask app
EXPOSE 8061

# Copy the rest of the application code
COPY . .

# Command to run the Flask app
CMD ["python3", "train_service_server.py"]
