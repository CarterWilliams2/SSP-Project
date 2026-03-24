import unittest
from ssp_project import validate_input_files, construct_zero_shot_prompt, construct_few_shot_prompt


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
        
    
    
    
if __name__ == '__main__':
    unittest.main()