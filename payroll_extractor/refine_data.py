import re
import sys
from extract_data import extract_totals

def refine_totals(sample_total):
    new_lines = []

    # We need a little hack to differentiate between the two different kinds of Medicare and Social Security
    medicare = False
    social_security = False
    for line in sample_total:
        line = split_401s(line)
        line = remove_commas(line)
        line = remove_hours(line)
        line = separate_words_from_dollars(line)
        line = itentify_paychex(line)
        #Differentiate between EE and ER Medicare
        if "Medicare" in line:
            if not medicare:
                medicare = True
                line = line.replace("Medicare", "EEMedicare")
            else:
                line = line.replace("Medicare", "ERMedicare")
        
        #Differentiate between EE and ER Social Security
        if "Social Security" in line:
            if not social_security:
                social_security = True
                line = line.replace("Social Security", "EESocial Security")
            else:
                line = line.replace("Social Security", "ERSocial Security")

        new_lines.append(line)
    return new_lines




#These are the individual steps required to refine the data for accurate extraction.

# Separate 401DLR, 401PCT, 401kDLR, 401kPCT and 401k if they are concatenated with other text
def split_401s(line):
    if "401DLR" in line:
        line = line.replace("401DLR", " 401DLR")
    if "401PCT" in line:
        line = line.replace("401PCT", " 401PCT")
    if "401kDLR" in line:
        line = line.replace("401kDLR", " 401kDLR")
    if "401kPCT" in line:
        line = line.replace("401kPCT", " 401kPCT")
    if "401k" in line:
        line = line.replace("401k", " 401k")
    return line


def remove_commas(line):
    return line.replace(',', '')

# Remove any number that has more than two decimal places (these are likely hours worked, not dollar amounts)
def remove_hours(line):
    parts = line.split()
    refined_parts = []
    for part in parts:
        if re.match(r'^\d+\.\d{3,}$', part):
            continue
        refined_parts.append(part)
    return ' '.join(refined_parts)

# Seperate words from dollars
def separate_words_from_dollars(line):
    parts = line.split()
    refined_parts = []
    for part in parts:
        # Use regex to add space between letters and numbers, except for 401DLR, 401kLoan, 401PCT, 401kDLR, and 401kPCT
        if part not in ("401DLR", "401kLoan", "401PCT", "401kDLR", "401kPCT"):
            part = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', part)
            part = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', part)
        refined_parts.append(part)
    return ' '.join(refined_parts)


#Identify paychex total
def itentify_paychex(line):
    return re.sub(r'(\s\d.*?)TOTAL', r'\1PayChexTotal', line)






#Test the refine_totals function for a specific totals section from a PDF
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python refine_data.py <pdf_path> <totals_section>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    totals_section = sys.argv[2]

    raw_totals = extract_totals(pdf_path)

    refined = refine_totals(raw_totals[totals_section])

    for line in refined:
        print(line)