import argparse
import fitz  # PyMuPDF

def pdf_to_html(pdf_file, html_file):
    doc = fitz.open(pdf_file)
    html = ""
    for page in doc:
        html += page.get_text("html")
    with open(html_file, "w") as f:
        f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to HTML")
    parser.add_argument("input_file", help="Input PDF file name")
    parser.add_argument("output_file", help="Output HTML file name")
    args = parser.parse_args()

    pdf_to_html(args.input_file, args.output_file)
