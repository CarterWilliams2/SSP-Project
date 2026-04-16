# SSP-Project
COMP 5700 Secure Software Project

## Team Members
| Carter Williams | cjw0113@auburn.edu | 904246901 
| Sathvik Prahadeeswaran | srp0061@auburn.edu | 904226136

## LLM Used (Task 1)
**google/gemma-3-1b-it** via Hugging Face Transformers

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests
```bash
pytest test_ssp_project.py -v
```

## Running the Binary
```bash
./ssp_project_binary <file1.pdf> <file2.pdf>
```
