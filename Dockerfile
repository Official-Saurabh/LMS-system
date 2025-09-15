FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional, keep image small). Uncomment if you need locales/ffmpeg etc.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     tzdata \
#  && rm -rf /var/lib/apt/lists/*

# Copy only application code (use .dockerignore to trim context)
COPY app ./app
COPY run.py ./
COPY config.json ./

# Install Python deps
RUN pip install --no-cache-dir Flask==3.0.0

# Expose the port the app runs on
EXPOSE 5000

# By default, run the Flask app
CMD ["python", "run.py"]

