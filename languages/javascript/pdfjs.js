const fs = require('fs');
const PDFJS = require('pdfjs-dist/es5/build/pdf');

// Path to the PDF file you want to convert
const pdfFilePath = 'path/to/your/pdf/file.pdf';

// Read the PDF file
fs.readFile(pdfFilePath, (err, data) => {
  if (err) {
    console.error('Error reading PDF file:', err);
    return;
  }

  // Convert data buffer to typed array
  const pdfData = new Uint8Array(data);

  // Load the PDF document
  PDFJS.getDocument(pdfData).promise.then(pdf => {
    // Initialize options for rendering
    const options = {
      // Set PDF scale
      scale: 1.5,
      // Enable text layer for better text rendering
      textLayer: true
    };

    // Initialize the HTML element where the PDF will be rendered
    const container = document.createElement('div');
    container.id = 'pdf-container';
    document.body.appendChild(container);

    // Render each page
    for (let i = 1; i <= pdf.numPages; i++) {
      pdf.getPage(i).then(page => {
        // Set up canvas for rendering
        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        // Render the page into the canvas
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: options.scale });
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        page.render({ canvasContext: context, viewport: viewport });

        // Extract text content if enabled
        if (options.textLayer) {
          page.getTextContent().then(textContent => {
            // Set up text layer
            const textLayerDiv = document.createElement('div');
            textLayerDiv.className = 'textLayer';
            container.appendChild(textLayerDiv);
            const textLayer = new PDFJS.TextLayerBuilder({
              textLayerDiv: textLayerDiv,
              pageIndex: page.pageIndex,
              viewport: viewport
            });
            textLayer.setTextContent(textContent);
            textLayer.render();
          });
        }
      });
    }
  }).catch(error => {
    console.error('Error loading PDF document:', error);
  });
});
