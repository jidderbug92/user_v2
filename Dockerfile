# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set environment variables (important for Flask)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# 3. Set working directory
WORKDIR /code

# Install system dependencies, including PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app code
COPY . .

# 6. Expose the Flask default port
EXPOSE 5000

# 7. Start Flask app (this keeps the container alive)
CMD ["flask", "run"]
