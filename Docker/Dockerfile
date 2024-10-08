FROM python:3.7-slim as python-base

WORKDIR /app
RUN apt-get update && \
   apt-get install -y procps && \
   apt-get install -y git && \
   apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/gerstung-lab/postcode && \
   cd postcode && \
   python3 -m pip install -e .


