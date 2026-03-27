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
    # initialize dicts
    dict1 = None
    dict2 = None
    
    # try to open the first file and turn to dict
    try:
        with open(file1, 'r') as yaml1:
            dict1 = yaml.safe_load(yaml1)
    except:
        print('Error opening the first file')
        
    # try to open the second file and turn to dict
    try:
        with open(file2, 'r') as yaml2:
            dict2 = yaml.safe_load(yaml2)
    except:
        print('Error opening the second file')
        
    # return the two dicts
    return dict1, dict2

# function that compares the two dicts from the yamls and reports on key data element differences
def key_data_diff(dict1, dict2, output_path):
    # initialize the names sets
    names1 = set()
    names2 = set()
    different_names = set()
    
    # iterate through elements of first dict and get the set of names
    for element in dict1:
        names1.add(element['name'])
    
    # iterate through elements of second dict and get the set of names
    for element in dict2:
        names2.add(element['name'])
    
    # check which names are one but not the other
    different_names += names1 - names2
    different_names += names2 - names1
    
    # write the differences to a text file
    with open(output_path, 'w') as file:
        # only write differences if there are any
        if len(different_names) > 0:
            # convert to list to iterate over and write to file
            different_names = list(different_names)
            for name in different_names:
                file.write(name)
                file.write('\n')
        else:
            file.write('NO DIFFERENCES IN REGARDS TO ELEMENT NAMES')

    return None