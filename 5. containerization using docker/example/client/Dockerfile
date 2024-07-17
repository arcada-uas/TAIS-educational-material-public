# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Copy the rest of the application code
COPY . .

# Command to run the client
CMD ["wait-for-it.sh", "data-server:8080", "--", "wait-for-it.sh", "train-server:8081", "--", "wait-for-it.sh", "test-server:8082", "--", "python", "client.py"]
