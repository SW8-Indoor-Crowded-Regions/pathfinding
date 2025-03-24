# Use Python 3.11.9 slim image
FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the FastAPI port
EXPOSE 8001

# Default: Run Uvicorn for development (with live reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
