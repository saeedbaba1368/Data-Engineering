#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_pdf> <output_html>"
    exit 1
fi

# Store input arguments
input_pdf="$1"
output_html="$2"

# Execute Pdf2Dom to convert PDF to HTML
java -jar pdf2dom.jar "$input_pdf" "$output_html"
