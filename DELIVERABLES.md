# Deliverables

## Task 1

1. `PROMPT.md` is in main directory, also in `./task-1`
2. YAML file outputs are in `./task-1/yaml-outputs`
3. Source code for six functions in `ssp_project.py`
    1. Input validation function: `validate_input_files`
    2. Zero shot prompt constructor: `construct_zero_shot_prompt`
    3. Few shot prompt constructor: `construct_few_shot_prompt`
    4. Chain of thought prompt constructor: `construct_chain_of_thought_prompt`
    5. LLM usage function: `run_llm_on_documents`
    6. Collect and dump LLM output: `dump_llm_output`
4. Test cases for six functions in `test_ssp_project.py`

## Task 2

1. Output text files in ./task-2
2. Source code for three functions in `ssp_project.py`
    1. Input function: `yaml_to_dict`
    2. KDE diff function: `key_data_diff`
    3. Req diff function: `data_requirements_diff`
3. Test cases for three functions in `test_ssp_project.py`

## Task 3

1. CSV file in ./task-3
2. Source code for four functions in `ssp_project.py`
    1. Input function: `task_three_input_function`
    2. Execute kubescape functions: `identify_kubescape_controls`, `execute_kubescape`
    3. CSV generation function: `generate_csv`
3. Test cases for three function in `test_ssp_project.py`

## Task 4

1. Public GitHub repo: [Repo Link](https://github.com/CarterWilliams2/SSP-Project)
2. GitHub Action file: [Check Actions tab to see all attempted pushes with test execution](https://github.com/CarterWilliams2/SSP-Project/actions)
3. Binary: `./dist/ssp_project/binary`
    Note: python source code for this in `main.py`; instructions in `README.md` on how to run
4. Requirement file: `requirements.txt`
