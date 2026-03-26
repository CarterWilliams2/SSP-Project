# Main file for our project
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import yaml

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

# function to construct a few shot prompt
# takes the files/file names as input
def construct_few_shot_prompt(file1, file2):
    # initialize prompt with zero shot as base
    prompt = construct_zero_shot_prompt(file1, file2)
    
    # make it few shot by adding examples of expected output
    prompt += ". For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }"
    prompt += ". Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}"
    
    return prompt

# function to construct a chain of thought prompt
# takes the files/file names as input
def construct_chain_of_thought_prompt(file1, file2):
    # true base
    prompt = ""
    
    # give it a role
    prompt += "You are a thorough Cybersecurity Engineer. "
    
    # add to prompt with few shot as base
    prompt += construct_few_shot_prompt(file1, file2)
    
    # make it chain of thought by adding thinking out loud
    prompt += ". Please think out loud as you go and detail your reasoning."
    
    return prompt

# function to dump the output of the models into a text file
# takes the model name, list of prompts, list of outputs, and name of output file as input
def dump_llm_output(model_name, prompts, outputs, file_out_name):
    # for each file we use these three prompt types
    prompt_types = ["Zero Shot", "Few Shot", "Chain of Thought"]
    
    # open up the output file
    with open(file_out_name, 'w') as file:
        # iterate through the prompts and outputs
        for i in range(len(prompt_types)):
            file.write("*LLM Name*\n")
            file.write(model_name)
            file.write("\n")
            file.write("*Prompt Used*\n")
            file.write(prompts[i])
            file.write("\n")
            file.write("*Prompt Type*\n")
            file.write(prompt_types[i]) 
            file.write("\n")
            file.write("*LLM Output*\n")
            file.write(outputs[i])
            file.write("\n")

    # return nothing
    return None

# function that automatically takes the two output files from task 1 as input
# turns them into dictionaries to make next two functions easier
def yaml_to_dict(file1, file2):
    # try to open the first file and turn to dict
    
    # try to open the second file and turn to dict
    
    # return the two dicts
    return None