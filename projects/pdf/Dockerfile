# Use the latest Python image as the base
FROM python:latest

# Install the required system dependencies
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install PyMuPDF package
RUN pip install PyMuPDF

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY script.py .

# Define the command to run the script
# CMD ["python", "script.py"]

# Start bash shell by default
CMD ["/bin/bash"]
