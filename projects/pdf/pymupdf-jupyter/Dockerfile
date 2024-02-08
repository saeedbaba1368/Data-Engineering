# Use the latest Python image as the base
FROM python:latest

# Install the required system dependencies
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    && apt-get install -y nodejs npm \
    && npm install -g npm@latest \
    && npm install -g configurable-http-proxy \
    && pip install jupyterlab

# Install PyMuPDF package
RUN pip install PyMuPDF

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY script.py .

# Expose port 8080 for JupyterLab
EXPOSE 8080

# Start bash by default
CMD ["/bin/bash"]
