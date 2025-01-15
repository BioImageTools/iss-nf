FROM condaforge/mambaforge

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mamba install python=3.10

# complex dependencies that needs to be solved with conda
RUN mamba install -c conda-forge gcc libgdal gxx imagecodecs -y

# satellite spatialdata projects
RUN pip install --no-cache-dir \
    spatialdata \
    spatialdata-io \
    spatialdata-plot

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Default command to run the Python script
# CMD ["python"]
