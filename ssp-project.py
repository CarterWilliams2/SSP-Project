# Main file for our project
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# input validation function
# takes two pdfs and applies adequate input validation measures
def validate_inpute_files(file1, file2):
    # try to open file1
    try:
        PdfReader(file1)
    except:
        PdfReadError("Invalid first PDF file")
    
    #try to open file2
    try:
        PdfReader(file2)
    except:
        PdfReadError("Invalid second PDF file")
    
    return None