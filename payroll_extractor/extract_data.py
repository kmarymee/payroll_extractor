import re
import sys
import pdfplumber

REPATTERN = r'^(\d{2}[A-Z]+TOTALS)$'


# Parse the PDF and extract totals sections
def extract_totals(pdf_path):
    print(f"Extracting data from {pdf_path}...")
    raw_totals = {}
    with pdfplumber.open(pdf_path) as pdf:
        write_totals = False
        for page in pdf.pages:
            lines = page.extract_text_lines()
            for line in lines:

                
                if re.match(REPATTERN, line['text']): # This indicates the beginning of a totals section
                    write_totals = line['text']
                    raw_totals[write_totals] = []
                    continue
                elif write_totals and line['text'].startswith('****'): # This indicates the end of a totals section
                    write_totals = False
                    continue
                elif line['text'] == 'COMPANYTOTALS': # This indicates the end of the final totals section
                    return raw_totals

                if write_totals:
                    raw_totals[write_totals].append(line['text']) # Store the line from this totals section 

    return raw_totals

# Debugging code to run the script and print the extracted totals data
# Provide a second argument of "raw" to print the raw totals data without refining or organizing it
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_data.py <pdf_path> <raw?>")
        sys.exit(1)

    if len(sys.argv) > 2 and sys.argv[2].lower() == "raw":
        print("Extracting raw totals data...")
        pdf_path = sys.argv[1]
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for line in page.extract_text_lines():
                    print(line['text'])

    else:
        pdf_path = sys.argv[1] 
        totals_data = extract_totals(pdf_path)
        for section, lines in totals_data.items():
            print(f"Section: {section}")
            for line in lines:
                print(f"  {line}")