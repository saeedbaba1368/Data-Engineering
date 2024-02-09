# Use an appropriate base image
FROM openjdk:11-jre-slim

# Set working directory in the container
WORKDIR /app

# Download Pdf2Dom JAR file
RUN apt-get update && \
    apt-get install -y wget && \
    wget --no-check-certificate https://downloads.sourceforge.net/project/cssbox/Pdf2DOM/2.0.0/PDFToHTML.jar -O pdf2dom.jar && \
    ls -l && \
    apt-get remove -y wget && \
    apt-get clean

# Set entry point to an interactive shell
ENTRYPOINT ["/bin/bash"]