
# Extract specific data points from the refined totals
def extract_point(data, key):
    for line in data:
        if key in line:
            return line.split(key)[1].strip().split()[0]

def organize_data(refined_data):
    data = {}

    data['WITHHOLDING'] = {}
    data['DEDUCTIONS'] = {} 
    data['WAGES & SALARIES'] = {}
    data['LIABILITIES'] = {}


    #This function will insert a key-value pair into the specified table, 
    # where the value is extracted from the refined data using the provided key
    def insert(table,key):
        table[key] = extract_point(refined_data, key)

    #This function will insert a key-value pair into the specified table, 
    # where the value is the sum of the values extracted from the refined data using the provided keys.
    # Specifically for 401PCT and 401kPCT, and 401DLR and 401kDLR, which need to be combined into singular fields.
    def insert_combined(table, key1, key2, combined_key):
        value1 = extract_point(refined_data, key1)
        value2 = extract_point(refined_data, key2)

        if value1 and value2:
            table[combined_key] = str(float(value1) + float(value2))
        elif value1:
            table[combined_key] = value1
        elif value2:
            table[combined_key] = value2
        else:
            table[combined_key] = None

    # Populate WITHHOLDING data
    insert(data['WITHHOLDING'], 'EESocial Security')
    insert(data['WITHHOLDING'], 'EEMedicare')
    insert(data['WITHHOLDING'], 'Fed Income Tax')
    insert(data['WITHHOLDING'], 'WA Cares LTC')
    insert(data['WITHHOLDING'], 'WA EE PFL')
    insert(data['WITHHOLDING'], 'WA EE PML')
    insert(data['WITHHOLDING'], 'EE WA L&I')


    # Populate DEDUCTIONS data
    insert(data['DEDUCTIONS'], 'AFLAC-pretax')
    insert(data['DEDUCTIONS'], 'PrincipalPostTax')
    insert(data['DEDUCTIONS'], 'Medical')

    #The float values of 401PCT and 401kPCT need to be combined in to a singular field, 401PCT
    insert_combined(data['DEDUCTIONS'], '401PCT', '401kPCT', '401PCT')

    insert(data['DEDUCTIONS'], '401kLoan')

    #The float values of 401DLR and 401kDLR need to be combined in to a singular field, 401DLR
    insert_combined(data['DEDUCTIONS'], '401DLR', '401kDLR', '401DLR')

    insert(data['DEDUCTIONS'], 'RthFlat')
    insert(data['DEDUCTIONS'], 'Rth 401 k')
    # insert(data['DEDUCTIONS'], '!IRA_Roth!')  #IRA Roth, unused but left in for ease of copy-paste
    insert(data['DEDUCTIONS'], 'Garnishment')
    insert(data['DEDUCTIONS'], 'Dental')
    insert(data['DEDUCTIONS'], 'EmployeeAdvance')
    insert(data['DEDUCTIONS'], 'PayChexTotal')

    # Populate WAGES & SALARIES data
    insert(data['WAGES & SALARIES'], 'Bonus')
    insert(data['WAGES & SALARIES'], 'Commission')
    insert(data['WAGES & SALARIES'], 'TOTAL')


    # Populate LIABILITIES data
    insert(data['LIABILITIES'], 'ERSocial Security')
    insert(data['LIABILITIES'], 'ERMedicare')
    insert(data['LIABILITIES'], 'Fed Unemploy')
    insert(data['LIABILITIES'], 'WA ER PML')
    insert(data['LIABILITIES'], 'WA Unemploy')
    insert(data['LIABILITIES'], 'WA Emp Adm Fund')
    insert(data['LIABILITIES'], 'ER WA L&I')

    # Save a place for the sum of the columns
    data['WITHHOLDING']['SUM'] = None
    data['DEDUCTIONS']['SUM'] = None
    data['LIABILITIES']['SUM'] = None

    return data



def print_data(data):
    # Print the organized data
    for category, items in data.items():
        print(f"{category}:")
        for key, value in items.items():
            print(f"  {key}: {value}")
        print()