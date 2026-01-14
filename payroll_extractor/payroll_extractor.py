import sys
from assemble_document import assemble_document

if __name__ == "__main__":
    if len(sys.argv) != 2:
        for arg in sys.argv:
            print(f"Argument: {arg}")
        print("Invalid Arguments.")
        print("Usage: python payroll_extractor.py <pdf_path>")
        print("Ensure your .pdf file is in the correct directory and does not have spaces in its name.")
        sys.exit(1)



    pdf_path = sys.argv[1]
    assemble_document(pdf_path)
    print("Done!")
    print(f"Payroll data extracted from {pdf_path} successfully!")
    sys.exit(0)

