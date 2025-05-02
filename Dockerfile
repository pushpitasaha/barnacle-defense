# Use official Python image
FROM python:3.10-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "webapp/app.py"]
