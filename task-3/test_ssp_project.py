import unittest
import os
import json
import tempfile
import zipfile
from unittest.mock import patch, MagicMock
from ssp_project import validate_input_files, construct_zero_shot_prompt, construct_few_shot_prompt, construct_chain_of_thought_prompt, dump_llm_output, run_llm_on_documents, yaml_to_dict, key_data_diff, data_requirements_diff, task_three_input_function, identify_kubescape_controls, execute_kubescape, generate_csv


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
        
    def test_run_llm_on_documents(self):
        # mock pipe returns a minimal YAML structure without loading the real model
        yaml_response = (
            "element1:\n"
            "  name: Title\n"
            "  requirements:\n"
            "    - descriptive\n"
            "    - concise\n"
        )

        def mock_pipe(messages, max_new_tokens=512):
            return [{'generated_text': messages + [{'role': 'assistant', 'content': yaml_response}]}]

        file1 = "./pdf-inputs/cis-r1.pdf"
        file2 = "./pdf-inputs/cis-r2.pdf"

        prompts, outputs, yaml1, yaml2 = run_llm_on_documents(
            file1, file2, output_dir="./test-files", _pipe=mock_pipe
        )

        assert len(prompts) == 3
        assert len(outputs) == 3
        assert yaml1.endswith(".yaml")
        assert yaml2.endswith(".yaml")
        assert yaml1 != yaml2
        assert os.path.exists(yaml1)
        assert os.path.exists(yaml2)

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
        dict1 = {'element1': {'name': 'title', 'requirements': ['one', 'two', 'three']}}
        dict2 = {'element1': {'name': 'title', 'requirements': ['four', 'five']}, 'element2': {'name': 'headers', 'requirements': ['six', 'seven']}}
        output_path = './test-files/task-two-req-diff.txt'
        
        # call the function
        data_requirements_diff(dict1, dict2, output_path)
        
        # mock the expected output
        # I am making it a set because there is no garuanteed ordering with symmetric difference
        expected = set(['title, one', 'title, two', 'title, three', 'title, four', 'title, five'])
        
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

    def test_identify_kubescape_controls(self):
        # use the real task-2 output files
        content1, content2 = task_three_input_function(
            './task-2/name-diff.txt',
            './task-2/req-diff.txt'
        )
        output_path = './test-files/test-controls.txt'

        controls = identify_kubescape_controls(content1, content2, output_path)

        # name-diff has real differences so controls should not be empty
        assert len(controls) > 0
        with open(output_path, 'r') as f:
            content = f.read()
        assert content != 'NO DIFFERENCES FOUND'

    def test_execute_kubescape(self):
        import pandas as pd

        # create a minimal yamls zip
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
            zip_path = tmp.name
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('pod.yaml', 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: test\nspec:\n  containers:\n  - name: c\n    image: nginx\n')

        # create a controls file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write('C-0013\nC-0057')
            controls_path = tmp.name

        # mock kubescape JSON output
        mock_results = {
            'summaryDetails': {
                'controls': {
                    'C-0013': {
                        'name': 'Non-root containers',
                        'severity': 'Medium',
                        'complianceScore': 0,
                        'ResourceCounters': {'failedResources': 1, 'passedResources': 0, 'skippedResources': 0}
                    }
                }
            }
        }

        def mock_run(cmd, **kwargs):
            out_idx = cmd.index('--output') + 1
            with open(cmd[out_idx], 'w') as f:
                json.dump(mock_results, f)

        with patch('subprocess.run', side_effect=mock_run):
            df = execute_kubescape(controls_path, zip_path)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['FilePath', 'Severity', 'Control name', 'Failed resources', 'All Resources', 'Compliance score']
        assert len(df) == 1

        os.unlink(zip_path)
        os.unlink(controls_path)

    def test_generate_csv(self):
        import pandas as pd

        df = pd.DataFrame([{
            'FilePath': 'project-yamls.zip',
            'Severity': 'Medium',
            'Control name': 'Non-root containers',
            'Failed resources': 1,
            'All Resources': 2,
            'Compliance score': 50.0
        }])
        output_path = './test-files/test-results.csv'

        generate_csv(df, output_path)

        assert os.path.exists(output_path)
        with open(output_path, 'r') as f:
            lines = f.read().splitlines()
        assert lines[0] == 'FilePath,Severity,Control name,Failed resources,All Resources,Compliance score'
        assert len(lines) == 2
        
        
        
if __name__ == '__main__':
    unittest.main()