# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /gaussian_mixed_model_mms

# Create necessary directories for your project structure
RUN mkdir -p models scripts data/processed

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies required for scientific packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy specific project directories
COPY . .

# Create a volume for data persistence
VOLUME ["/gaussian_mixed_model_mms/data"]

# Set environment variable to prevent IMK messages on macOS
ENV PYTHONUNBUFFERED=1

# Set the entry point to run main.py
CMD ["python", "visualization/vis_v3.py"]