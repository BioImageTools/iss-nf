FROM python:3.7-slim as python-base

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the rest of the application code
COPY registration.py /scripts/registration.py

# Default command to run the Python script
# CMD ["python", "registration.py"]
