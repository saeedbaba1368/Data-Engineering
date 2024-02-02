import PyPDF2
import csv
import re

import tabula
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    # Read PDF into DataFrame using tabula
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

    return tables

def write_tables_to_csv(tables, csv_path):
    # Create a new Pandas DataFrame for each table
    dfs = [pd.DataFrame(table) for table in tables]

    # Write each DataFrame to a CSV file
    for i, df in enumerate(dfs):
        df.to_csv(f"{csv_path}_table_{i + 1}.csv", index=False)
        print(f"Table {i + 1} written to CSV.")




class PDFTableExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_tables(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages

            all_tables = []

            for page_number in range(num_pages):
                page = pdf_reader.getPage(page_number)
                text = page.extractText()

                tables = self.extract_tables_from_text(text)
                all_tables.extend(tables)

        return all_tables

    def extract_tables_from_text(self, text):
        tables = []

        # Define a simple rule for detecting tables based on lines
        table_lines = re.findall(r'\+-+\+', text)
        
        for table_line in table_lines:
            table_start_index = text.find(table_line)
            table_end_index = text.find(table_line, table_start_index + 1)

            if table_end_index != -1:
                table_text = text[table_start_index:table_end_index + len(table_line)].strip()
                table = self.construct_table_from_text(table_text)
                tables.append(table)

        return tables

    def construct_table_from_text(self, table_text):
        rows = [row.split('|')[1:-1] for row in table_text.split('\n') if row.strip()]

        # Assuming the first row contains headers
        headers = rows[0]
        data = rows[1:]

        return {'headers': headers, 'data': data}

    def write_tables_to_csv(self, tables, csv_path):
        for i, table in enumerate(tables):
            csv_file_path = f"{csv_path}_table_{i + 1}.csv"

            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(table['headers'])
                csv_writer.writerows(table['data'])

            print(f"Table {i + 1} written to CSV: {csv_file_path}")


if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the actual path to your PDF file
    pdf_file_path = 'your_pdf_file.pdf'

    # Replace 'output_csv_file' with the desired name for the CSV file
    output_csv_file = 'output_csv_file'

    # Create an instance of PDFTableExtractor
    pdf_table_extractor = PDFTableExtractor(pdf_file_path)

    # Extract tables from the PDF
    extracted_tables = pdf_table_extractor.extract_tables()

    # Write tables to CSV
    pdf_table_extractor.write_tables_to_csv(extracted_tables, output_csv_file)

    # using tabula
    # Extract tables from the PDF
    extracted_tables = extract_tables_from_pdf(pdf_file_path)

    # Write tables to CSV
    write_tables_to_csv(extracted_tables, output_csv_file)