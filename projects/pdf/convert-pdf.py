from pdfix import Pdfix
from pdfix.models import HtmlSaveOptions

def convert_pdf_to_html(pdf_path, html_path):
    pdfix = Pdfix()

    # Initialize PDFix
    if pdfix == None or not pdfix.Init():
        print("Failed to initialize PDFix SDK")
        return

    try:
        # Open the PDF document
        doc = pdfix.OpenDoc(pdf_path)
        if doc == None:
            print("Failed to open the PDF document")
            return
        
        try:
            # Initialize HTML save options
            save_options = HtmlSaveOptions()
            save_options.flags = HtmlSaveOptions.kHtmlNoExternalCSS | HtmlSaveOptions.kHtmlNoExternalJS

            # Save the PDF document as HTML
            if not doc.SaveAsHtml(html_path, save_options):
                print("Failed to save the PDF document as HTML")
                return
        finally:
            # Close the PDF document
            doc.Close()
    finally:
        # Destroy PDFix object
        pdfix.Destroy()

if __name__ == "__main__":
    # Specify the input PDF file path
    input_pdf_path = "input.pdf"
    
    # Specify the output HTML file path
    output_html_path = "output.html"
    
    # Convert PDF to HTML
    convert_pdf_to_html(input_pdf_path, output_html_path)
