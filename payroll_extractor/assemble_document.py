from assemble_data import assemble_data, get_departments, get_labels
import xlsxwriter
import sys
import shutil

def assemble_document(pdf_path):
    data = assemble_data(pdf_path)

    path, ext = pdf_path.rsplit('.', 1)
    doc_name = path.rsplit('\\', 1)[-1]  # Extract document name without path
    print(f"Outputting assembled data to {doc_name}.xlsx...")
    if ext.lower() != 'pdf':
        print("Error: The provided file is not a PDF.")
        sys.exit(1)

    #So we can navitage columns easily
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    departments = get_departments(data)

    # Create an Excel workbook and worksheet
    workbook = xlsxwriter.Workbook(f'{doc_name}_sheet.xlsx') 
    ws = workbook.add_worksheet(doc_name)

    # Assemble the spreadsheet to be in the correct format

    lable = workbook.add_format({'bold': True, 'align': 'center'})

    def create_header(range, title):
        # Create the format: bold + centered + light blue background
        header_format = workbook.add_format({
            'bold':     True,                  # Makes text bold
            'align':    'center',              # Horizontal center
            'valign':   'vcenter',             # Vertical center (good for merged cells)
            'bg_color': '#ADD8E6',           # Light blue (you can also use '#BFEFFF' or '#CCE5FF' for variations)
            # Optional extras you might like:
            'font_size': 12,
            'border': 1,                     # Thin border around merged area
        })

        # Merge A1:K1 and write text with the format
        # ws.merge_range('A1:K1', 'WITHHOLDING', header_format)
        ws.merge_range(range, title, header_format)

        # Optional: Widen columns if needed (A to K)
        # ws.set_column('A:K', 12)  # Adjust width as desired

    categories = ["WITHHOLDING", "DEDUCTIONS", "WAGES & SALARIES", "LIABILITIES"]
    start_row = 0  # 0-based

    for category in categories:
        labels = get_labels(data, category)
        if not labels:
            continue  # Skip if no labels for this category

        # Create header
        header_row = start_row + 1  # 1-based
        create_header(f'A{header_row}:{letters[len(departments)]}{header_row}', category)
        ws.set_row(header_row - 1, 30)  # set_row is 0-based

        # Department labels
        dept_row = header_row + 1
        for dept in departments:
            col_index = departments.index(dept) + 1  # +1 to account for column A being labels
            cell = f"{letters[col_index]}{dept_row}"
            ws.write_string(cell, dept, lable)

        # Label rows
        label_row_start = dept_row + 1
        for i, label in enumerate(labels):
            row = label_row_start + i
            cell = f"A{row}"
            ws.write_string(cell, label, lable)

        # Fill in data
        for i, dept in enumerate(list(data.keys())):
            for j, label in enumerate(labels):
                row = label_row_start + j
                col_index = i + 1  # +1 to account for column A being labels
                cell = f"{letters[col_index]}{row}"
                number_format = workbook.add_format({'num_format': '0.00'})
                if label == "SUM":
                    start_cell = f"{letters[col_index]}{label_row_start}"
                    end_cell = f"{letters[col_index]}{row-1}"
                    formula = f"=SUM({start_cell}:{end_cell})"
                    ws.write_formula(cell, formula, number_format)
                elif data[dept][category][label]:

                    #dirty fix. Removes those asterisks that throw off the float conversion.
                    value_to_float = data[dept][category][label]
                    if "*" in value_to_float:
                        value_to_float = value_to_float.replace("*","")

                    #Let the user know something is wrong if the value can't be converted to float.
                    floated_value = 0
                    try:
                        floated_value = float(value_to_float)
                        ws.write_number(cell, floated_value, number_format)
                    except (ValueError):
                        cell_format = workbook.add_format({'bg_color': '#D0342C'})
                        ws.write(cell, f'{value_to_float}??', cell_format)
                        print(f"WARNING!!! Value '{value_to_float}' in cell {cell} cannot be interpreted numerically!")
                    

        # Update start_row for next category
        start_row = label_row_start + len(labels) - 1  # 0-based, last row used

    # Set column A width to 20 for better readability
    ws.set_column('A:A', 20)

    # Add border around cells to improve readability
    border_format = workbook.add_format({'border': 1})
    # Apply border to all data areas - this is simplified, you might need to adjust ranges
    # For now, apply to a large range
    ws.conditional_format('A1:Z100', {'type': 'cell', 'criteria': '!=', 'value': '', 'format': border_format})



    workbook.close()
    
    # Move the created workbook to the desired output path
    # shutil.move(f'{doc_name}_sheet.xlsx', output_path)

# assemble_document('PPE 110925.pdf', 'PPE 110925.xlsx')