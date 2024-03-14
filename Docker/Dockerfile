FROM python:3.7-slim as python-base

WORKDIR /app
RUN apt-get update && \
   apt-get install -y procps && \
   apt-get clean
COPY requirements_.txt .
RUN pip install --no-cache-dir -r requirements.txt
