import fitz  # PyMuPDF

def extract_table_like_structure(pdf_file):
    doc = fitz.open(pdf_file)
    table_structures = []

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        blocks = page.get_text("blocks")

        table = []
        row = []

        for b in blocks:
            _, _, block_width, block_height, block_text, _ = b
            # Arbitrarily chosen threshold to consider a block as a table cell
            if block_width > 20 and block_height > 10:
                row.append(block_text.strip())
            else:
                if row:
                    table.append(row)
                    row = []

        if table:
            table_structures.append(table)

    return table_structures

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract table-like structures from a PDF document")
    parser.add_argument("input_file", help="Input PDF file name")
    args = parser.parse_args()

    table_structures = extract_table_like_structure(args.input_file)
    if table_structures:
        for i, table in enumerate(table_structures):
            print(f"Table {i+1}:")
            for row in table:
                print("\t".join(row))
            print()
    else:
        print("No table-like structures found.")
