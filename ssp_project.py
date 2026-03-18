# Main file for our project
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# input validation function
# takes two pdfs and applies adequate input validation measures
def validate_input_files(file1, file2):
    errors = 0
    
    # try to open and extract from file1
    try:
        read1 = PdfReader(file1)
        page1 = read1.pages[0]
        print(page1)
    except:
        PdfReadError("Invalid first PDF file")
        errors += 1
    
    #try to open and extract from file2
    try:
        read2 = PdfReader(file2)
        page2 = read2.pages[0]
        print(page2)
    except:
        PdfReadError("Invalid second PDF file")
        errors += 1
    
    print(errors, " error(s)")
    
    return errors
