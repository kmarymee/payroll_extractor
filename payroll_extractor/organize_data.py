
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



    def insert(table,key):
        table[key] = extract_point(refined_data, key)

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
    insert(data['DEDUCTIONS'], '401PCT')
    insert(data['DEDUCTIONS'], '401kLoan')
    insert(data['DEDUCTIONS'], '401DLR')
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