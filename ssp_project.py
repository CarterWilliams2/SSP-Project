# Main file for our project
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# input validation function
# takes two pdfs and applies adequate input validation measures
def validate_input_files(file1, file2):
    errors = 0
    
    # try to open file1
    try:
        PdfReader(file1)
    except:
        PdfReadError("Invalid first PDF file")
        errors += 1
    
    #try to open file2
    try:
        PdfReader(file2)
    except:
        PdfReadError("Invalid second PDF file")
        errors += 1
    
    print(errors, " error(s)")
    
    return errors
