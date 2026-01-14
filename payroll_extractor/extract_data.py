import re
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
                    # print(f"Begin totals section: {line['text']}")
                    write_totals = line['text']
                    raw_totals[write_totals] = []
                    continue
                elif write_totals and line['text'].startswith('****'): # This indicates the end of a totals section
                    # print(f"End of totals section {write_totals} at {line['text']}")
                    write_totals = False
                    continue
                elif line['text'] == 'COMPANYTOTALS':
                    # print('End of all totals sections reached.')
                    break

                if write_totals:
                    raw_totals[write_totals].append(line['text']) # Store the line from this totals section 

    return raw_totals
