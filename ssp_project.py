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
    
    # try to open and extract from file2
    try:
        read2 = PdfReader(file2)
        page2 = read2.pages[0]
        print(page2)
    except:
        PdfReadError("Invalid second PDF file")
        errors += 1
    
    print(errors, " error(s)")
    
    return errors

# function to construct a zero-shot prompt
# takes the files/file names as input
def construct_zero_shot_prompt(file1, file2):
    # initialize prompt
    prompt = ""
    # base of prompt
    prompt += "Please analyze the following two documents to identify key data elements: "
    # add file names
    prompt += file1 + " and " + file2 + ". "
    # specify output structure
    prompt += "Structure your output as a nested dictionary with the following structure: "
    prompt += "{element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }"
    
    return prompt

def construct_few_shot_prompt(file1, file2):
    # initialize prompt with zero shot as base
    prompt = construct_zero_shot_prompt(file1, file2)
    
    # make it few shot by adding examples of expected output
    prompt += ". For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }"
    prompt += ". Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}"
    
    return prompt