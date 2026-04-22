# SSP-Project

COMP 5700 Secure Software Project

## Team Members

| Carter Williams | `cjw0113@auburn.edu` | 904246901
| Sathvik Prahadeeswaran | `srp0061@auburn.edu` | 904226136

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

Please ensure you have git-lfs and kubescape tools installed.
git-lfs: [download instructions](https://git-lfs.com)
kubescape: [download instructions](https://kubescape.io/docs/install-cli/)

```bash
git lfs install
git lfs pull
./ssp_project_binary <file1.pdf> <file2.pdf>
```

Note: `project-yamls.zip` must be in the same directory as the binary for the Kubescape scan (Task 3) to run.

Alternatively, you can build the binary yourself after activating your virtual environment and installing requirements.

```bash
pyinstaller --onefile main.py -n ssp_project_binary
```

## Deliverables

More information about all deliverables available in `DELIVERABLES.md`

## AI Usage Declartion

AI Usage Declaration found in `AI_USAGE_DECLARATION.txt`
