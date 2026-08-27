FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and enable real-time logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Flask listens on port 5000
EXPOSE 5000

# Start Flask
CMD ["python", "app.py"]