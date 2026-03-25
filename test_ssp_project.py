import unittest
from ssp_project import validate_input_files, construct_zero_shot_prompt, construct_few_shot_prompt, construct_chain_of_thought_prompt, dump_llm_output


class TestTask1Methods(unittest.TestCase):
    def test_validate_input_files(self):
        file1 = "./pdf-inputs/cis-r1.pdf"
        file2 = "./pdf-inputs/cis-r2.pdf"
        
        num_errors = validate_input_files(file1, file2)
        
        assert num_errors == 0
    
    def test_zero_show_prompt(self):
        file1 = "file1.pdf"
        file2 = "file2.pdf"
        
        zero_shot_prompt = "Please analyze the following two documents to identify key data elements: file1.pdf and file2.pdf. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }" 
        assert zero_shot_prompt == construct_zero_shot_prompt(file1, file2)
    
    def test_few_shot_prompt(self):
        file1 = "file1.pdf"
        file2 = "file2.pdf"
        
        few_shot_prompt = "Please analyze the following two documents to identify key data elements: file1.pdf and file2.pdf. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }. For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }. Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}"
        assert few_shot_prompt == construct_few_shot_prompt(file1, file2)
        
    def test_chain_of_thought_prompt(self):
        file1 = "file1.pdf"
        file2 = "file2.pdf"
        
        chain_of_thought_prompt = "You are a thorough Cybersecurity Engineer. Please analyze the following two documents to identify key data elements: file1.pdf and file2.pdf. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }. For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }. Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}. Please think out loud as you go and detail your reasoning."
        assert chain_of_thought_prompt == construct_chain_of_thought_prompt(file1, file2)
        
    def test_dump_llm_output(self):
        # mock inputs
        model_name = "M1"
        prompts = ["Prompt1", "Prompt-2", "PROMPT #3"]
        outputs = ["Output1", "Output-2", "OUTPUT #3"]
        file_out_name = "test-dump-llm-output.txt"
        
        # call the function
        dump_llm_output(model_name, prompts, outputs, file_out_name)
        
        # open up the created output file
        with open(file_out_name, 'r') as file:
            content_created = file.read()
        
        # open up the mocked output file
        with open("expected-dump-llm-output.txt", 'r') as file:
            content_expected = file.read()
        
        # check to see if created output is equal to expected output
        assert content_created == content_expected
        
    
    
if __name__ == '__main__':
    unittest.main()