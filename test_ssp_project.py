import unittest
from ssp_project import validate_input_files


class TestVaildateInputFiles(unittest.TestCase):
    def test_validate_input_files(self):
        file1 = "./pdf-inputs/cis-r1.pdf"
        file2 = "./pdf-inputs/cis-r2.pdf"
        
        num_errors = validate_input_files(file1, file2)
        
        assert num_errors == 0
    
    
    
if __name__ == '__main__':
    unittest.main()