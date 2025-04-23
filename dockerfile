# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Update system packages
RUN apt-get update && apt-get install -y gcc

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY static/ ./static/
COPY checkpoint-5268/ ./checkpoint-5268/

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
