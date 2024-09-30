# Use an official Python runtime as the base image
FROM python:3.12-slim

# Install system dependencies required to build mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Create a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment and install dependencies
# Use bash to run the activation script to install dependencies in the virtual environment
RUN /app/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /app/venv/bin/pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application using the virtual environment
CMD ["/app/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
