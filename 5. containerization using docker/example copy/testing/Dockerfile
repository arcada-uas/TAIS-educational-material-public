# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports used by Flask and gRPC
EXPOSE 5000 8082

# Command to run both the Flask app and the gRPC server
CMD ["python", "test_service_server.py"]
