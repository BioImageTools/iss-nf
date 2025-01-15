FROM python:3.7-slim as python-base

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN git clone https://github.com/gerstung-lab/postcode && \
   cd postcode && \
   python3 -m pip install -e .

   # Copy the rest of the application code
COPY postcode_decoder.py /scripts/postcode_decoder.py
COPY exp_metadata_json.py /scripts/exp_metadata_json.py

# Default command to run the Python script
# CMD ["python", "postcode_decoder.py"]