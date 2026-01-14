# PAYROLL EXTRACTOR
### A python-based PDF processing tool for extracting accounting data from specific .PDF files

## Prerequisites
1. Ensure python is installed on the system.
2. Install the required packages listed in requirements.txt
    - Navigate to the directory where requirements.txt exists
    - Use pip to install the packages
    ```
    pip install -r requirements.txt
    ```

## Drag-and-Drop Usage
- Drag and drop a compatible .PDF file on to run_payroll.bat
- Ensure the file name and file **path** does not contain spaces.

## Command Line Usage
- Navigate to the directory where payroll_extractor.py exists.
- Run the script in python and provide the file path to the .PDF file you wish to process
EG:
    ```bat
    python payroll_extractor.py documents\payroll\010126.pdf
    ```
- Running the script from the command line will allow the file name and path to contain spaces.
- The script will then output the spreadsheet to the current directory.