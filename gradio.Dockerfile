FROM python:3.10-slim

WORKDIR /app

# Install required system packages first
RUN apt-get update && apt-get install -y build-essential

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "gradio_app.py"]