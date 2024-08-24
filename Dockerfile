# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Install system dependencies required for PyStemmer and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the necessary files and directories into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose ports for FastAPI and Dash apps
EXPOSE 4000 8000 8050

# Install gunicorn for running the Dash app
RUN pip install gunicorn uvicorn

# Assuming start_services.sh is properly written and in the same directory as the Dockerfile
COPY start_services.sh /app/start_services.sh
RUN chmod +x /app/start_services.sh

CMD ["/app/start_services.sh"]
