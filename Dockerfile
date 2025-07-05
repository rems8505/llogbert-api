FROM python:3.10-slim

WORKDIR /app

# Install required system packages first
RUN apt-get update && apt-get install -y build-essential

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Use full path to uvicorn to avoid path issues
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
