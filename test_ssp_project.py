import unittest
from ssp_project import validate_input_files, construct_zero_shot_prompt, construct_few_shot_prompt, construct_chain_of_thought_prompt, dump_llm_output, yaml_to_dict, key_data_diff, data_requirements_diff, task_three_input_function


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
        file_out_name = "./test-files/test-dump-llm-output.txt"
        
        # call the function
        dump_llm_output(model_name, prompts, outputs, file_out_name)
        
        # open up the created output file
        with open(file_out_name, 'r') as file:
            content_created = file.read()
        
        # open up the mocked output file
        with open("./test-files/expected-dump-llm-output.txt", 'r') as file:
            content_expected = file.read()
        
        # check to see if created output is equal to expected output
        assert content_created == content_expected
        
        
class TestTask2Methods(unittest.TestCase):    
    def test_yaml_to_dict(self):
        # mock inputs
        file1 = "./test-files/test1.yaml"
        file2 = "./test-files/test2.yaml"
        
        # call the function
        dict1, dict2 = yaml_to_dict(file1, file2)
        
        # make sure there was no error loading in the files
        assert dict1 is not None and dict2 is not None
    
    def test_key_data_diff(self):
        # mock inputs
        dict1 = {'element1': {'name': 'title', 'requirements': ['one', 'two', 'three']}}
        dict2 = {'element1': {'name': 'title', 'requirements': ['four', 'five']}, 'element2': {'name': 'headers', 'requirements': ['six', 'seven']}}
        output_path = './test-files/task-two-name-diff.txt'
        
        # call the function
        key_data_diff(dict1, dict2, output_path)
        
        # mock the expected output
        expected = ['headers']
        
        # open the test file and convert to a list
        with open(output_path, 'r') as file:
            content = file.read()
            actual = content.splitlines()
        
        assert expected == actual
    
    def test_data_requirements_diff(self):
        # mock inputs
        dict1 = {'element1': {'name': 'kde1', 'requirements': ['req1', 'req2', 'req3']}, 'element2': {'name': 'kde2', 'req': ['req4', 'req5']}}
        dict2 = {'element1': {'name': 'kde1', 'requirements': ['req1', 'req2']}, 'element2': {'name': 'kde3', 'requirements': ['req6', 'req7']}}
        output_path = './test-files/task-two-req-diff.txt'
        file1 = 'file1'
        file2 = 'file2'
        
        # call the function
        data_requirements_diff(dict1, dict2, output_path, file1, file2)
        
        # mock the expected output
        # I am making it a set because there is no garuanteed ordering with symmetric difference
        with open('./test-files/task-two-req-diff-mock.txt', 'r') as file:
            content = file.read()
            expected = set(content.splitlines())
            
        # open the test file and convert to a list
        with open(output_path, 'r') as file:
            content = file.read()
            actual = set(content.splitlines())
        
        assert expected == actual

class TestTask3Methods(unittest.TestCase):
    def test_task_three_input_function(self):
        # mock inputs
        file1 = './test-files/task-3-input1.txt'
        file2 = './test-files/task-3-input2.txt'
        
        # call the function
        actual1, actual2 = task_three_input_function(file1, file2)
        
        # mock outputs
        expected1 = "title\nclosing"
        expected2 = "title, length"
        
        assert actual1 == expected1 and actual2 == expected2
        
        
        
if __name__ == '__main__':
    unittest.main()