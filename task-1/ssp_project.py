# Main file for our project
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import yaml
import os
import re

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
        names1.add(dict1[element]['name'])
    
    # iterate through elements of second dict and get the set of names
    for element in dict2:
        names2.add(dict2[element]['name'])
    
    # check which names are one but not the other
    different_names = names1.symmetric_difference(names2)
    
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

# function that compares the two dicts from the yaml and reports on key data requirement differences
def data_requirements_diff(dict1, dict2, output_path):
    # initialize the sets of names and requirement difference array
    names1 = set()
    names2 = set()
    common_names = set()
    req_diff = []
    
    # iterate through elements of first dict and get the set of names
    for element in dict1:
        names1.add(dict1[element]['name'])
    
    # iterate through elements of second dict and get the set of names
    for element in dict2:
        names2.add(dict2[element]['name'])
    
    # get the names that are in both dicts
    common_names = names1.intersection(names2)
    
    # get the differences in requirements
    for name in common_names:
        # initialize the requirements of each as a set
        req1 = set()
        req2 = set()
        difference_set = set()
        for element in dict1:
            if name == dict1[element]['name']:
                req1 = set(dict1[element]['requirements'])
        for element in dict2:
            if name == dict2[element]['name']:
                req2 = set(dict2[element]['requirements'])
        
        # find differences and add them to overall diff array
        difference_set = req1.symmetric_difference(req2)
        for diff in list(difference_set):
            req_diff.append(tuple([name, diff]))
    
    # write to the file
    with open(output_path, 'w') as file:
        # only write differences if there are any
        if len(req_diff) > 0:
            # write differences
            for name, req in req_diff:
                file.write(f'{name}, {req}')
                file.write('\n')
        else:
            file.write('NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS')
    
    return None

# function that uses Gemma-3-1B LLM with each prompt type to extract KDEs from two PDFs
# saves a YAML file per document and returns (prompts, outputs, yaml1_path, yaml2_path)
# _pipe is injectable for testing — if None, loads the real Gemma model
def run_llm_on_documents(file1, file2, output_dir='.', _pipe=None):
    if _pipe is None:
        from transformers import pipeline as hf_pipeline
        import torch
        _pipe = hf_pipeline(
            "text-generation",
            model="google/gemma-3-1b-it",
            device="cpu",
            torch_dtype=torch.bfloat16
        )

    # extract up to 5000 chars from the Recommendation Definitions section (index 11)
    def extract_pdf_text(pdf_path, start_page=11, max_chars=5000):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages[start_page:start_page + 10]:
            text += page.extract_text() or ""
            if len(text) >= max_chars:
                break
        return text[:max_chars]

    # call the LLM and return the assistant response string
    def call_llm(prompt_text):
        messages = [{"role": "user", "content": prompt_text}]
        result = _pipe(messages, max_new_tokens=512)
        return result[0]['generated_text'][-1]['content']

    # try to turn raw LLM output into a nested dict matching the KDE schema
    def parse_to_dict(output_text):
        # prefer a fenced YAML block
        match = re.search(r'```(?:yaml)?\n(.*?)```', output_text, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                parsed = yaml.safe_load(match.group(1))
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # fall back to the first element\d+: block we can find
        match = re.search(r'(element\d[\s\S]*)', output_text)
        if match:
            try:
                parsed = yaml.safe_load(match.group(1))
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # last resort: return a minimal valid structure
        return {'element1': {'name': 'Unknown', 'requirements': ['Could not parse LLM output']}}

    text1 = extract_pdf_text(file1)
    text2 = extract_pdf_text(file2)
    combined = f"Document 1 ({file1}):\n{text1}\n\nDocument 2 ({file2}):\n{text2}"

    # build all three prompts and collect raw LLM outputs (used for dump_llm_output)
    zero_shot = construct_zero_shot_prompt(file1, file2)
    few_shot = construct_few_shot_prompt(file1, file2)
    chain_of_thought = construct_chain_of_thought_prompt(file1, file2)
    prompts = [zero_shot, few_shot, chain_of_thought]

    outputs = []
    for prompt in prompts:
        outputs.append(call_llm(prompt + "\n\nDocument content:\n" + combined))

    # extract KDEs for each document individually using a YAML-focused prompt
    def extract_kdes(doc_text, doc_name):
        extraction_prompt = (
            "You are a thorough Cybersecurity Engineer. "
            "Analyze the following document and identify its key data elements. "
            "Output ONLY valid YAML using this exact structure:\n"
            "element1:\n  name: <element name>\n  requirements:\n    - <req1>\n    - <req2>\n"
            "element2:\n  name: <element name>\n  requirements:\n    - <req1>\n\n"
            f"Document ({doc_name}):\n{doc_text}"
        )
        return parse_to_dict(call_llm(extraction_prompt))

    dict1 = extract_kdes(text1, file1)
    dict2 = extract_kdes(text2, file2)

    # derive YAML file names from input PDF names
    def yaml_path(pdf_path, suffix=''):
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        return os.path.join(output_dir, f"{base}{suffix}-kdes.yaml")

    yaml1_path = yaml_path(file1)
    yaml2_path = yaml_path(file2)

    # when both files are the same, distinguish the outputs with -1 / -2
    if yaml1_path == yaml2_path:
        yaml1_path = yaml_path(file1, '-1')
        yaml2_path = yaml_path(file2, '-2')

    with open(yaml1_path, 'w') as f:
        yaml.dump(dict1, f, default_flow_style=False)

    with open(yaml2_path, 'w') as f:
        yaml.dump(dict2, f, default_flow_style=False)

    return prompts, outputs, yaml1_path, yaml2_path


# function that takes two text files from task 2 as input
# returns the content as strings
def task_three_input_function(file1, file2):
    # open the first file and turn into set
    with open(file1, 'r') as file:
        content1 = file.read()
        
        
    # open the second file and turn into set
    with open(file2, 'r') as file:
        content2 = file.read()
        
    
    return content1, content2