import sys
import pprint
from extract_data import extract_totals
from refine_data import refine_totals
from organize_data import organize_data, print_data


def get_departments(data):
    department_nums = []
    for department_name in data.keys():
        department_nums.append(department_name[:2])
    return department_nums

def get_labels(data, section):
    keys = list(data.keys())
    return list(data[keys[0]][section].keys())


def assemble_data(pdf_path):
    print("Assembling organized data...")
    #Extract totals from the PDF
    raw_totals = extract_totals(pdf_path)

    output = {}

    # For each totals section, refine and organize the data
    for k,v in raw_totals.items():
        refined_data = refine_totals(v)
        data = organize_data(refined_data)
        output[k] = data

    return output

# print(assemble_data('PPE 110925.pdf'))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python assemble_data.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    test = assemble_data(pdf_path)

    # print(get_departments(test))
    # print(get_labels(test, "WITHHOLDING"))
    # print(get_labels(test, "DEDUCTIONS"))
    # print(get_labels(test, "WAGES & SALARIES"))
    # print(get_labels(test, "LIABILITIES"))

    print(pprint.pformat(test))

    # # Print the assembled data
    # for section, data in test.items():
    #     print(f"Section: {section}")
    #     print_data(data)
    #     print()