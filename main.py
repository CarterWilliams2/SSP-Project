#!/usr/bin/env python3
"""
SSP-Project binary entry point.
Usage:
  Run a specific pair:   ssp_project_binary <file1.pdf> <file2.pdf>
  Run all nine inputs:   ssp_project_binary
"""
import sys
import os
from ssp_project import (
    validate_input_files,
    run_llm_on_documents,
    dump_llm_output,
    yaml_to_dict,
    key_data_diff,
    data_requirements_diff,
    task_three_input_function,
    identify_kubescape_controls,
    execute_kubescape,
    generate_csv,
)

NINE_INPUTS = [
    ("pdf-inputs/cis-r1.pdf", "pdf-inputs/cis-r1.pdf"),
    ("pdf-inputs/cis-r1.pdf", "pdf-inputs/cis-r2.pdf"),
    ("pdf-inputs/cis-r1.pdf", "pdf-inputs/cis-r3.pdf"),
    ("pdf-inputs/cis-r1.pdf", "pdf-inputs/cis-r4.pdf"),
    ("pdf-inputs/cis-r2.pdf", "pdf-inputs/cis-r2.pdf"),
    ("pdf-inputs/cis-r2.pdf", "pdf-inputs/cis-r3.pdf"),
    ("pdf-inputs/cis-r2.pdf", "pdf-inputs/cis-r4.pdf"),
    ("pdf-inputs/cis-r3.pdf", "pdf-inputs/cis-r3.pdf"),
    ("pdf-inputs/cis-r3.pdf", "pdf-inputs/cis-r4.pdf"),
]

YAMLS_ZIP = "project-yamls.zip"


def run_pipeline(file1, file2):
    base1 = os.path.splitext(os.path.basename(file1))[0]
    base2 = os.path.splitext(os.path.basename(file2))[0]
    pair  = f"{base1}-{base2}"

    output_dir = os.path.join("outputs", pair)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*55}")
    print(f" Processing: {file1} + {file2}")
    print(f"{'='*55}")

    # Task 1 - validate
    print("[Task 1] Validating input files...")
    errors = validate_input_files(file1, file2)
    if errors > 0:
        print(f"  ERROR: {errors} invalid file(s). Skipping pair.")
        return

    # Task 1 - LLM extraction
    print("[Task 1] Running LLM extraction (Gemma-3-1B)...")
    prompts, outputs, yaml1, yaml2 = run_llm_on_documents(
        file1, file2, output_dir=output_dir
    )
    print(f"  YAML outputs: {yaml1}, {yaml2}")

    # Task 1 - dump LLM output
    llm_dump = os.path.join(output_dir, f"{pair}-llm-output.txt")
    dump_llm_output("google/gemma-3-1b-it", prompts, outputs, llm_dump)
    print(f"  LLM dump: {llm_dump}")

    # Task 2 - compare YAMLs
    print("[Task 2] Comparing YAML files...")
    dict1, dict2 = yaml_to_dict(yaml1, yaml2)

    name_diff_path = os.path.join(output_dir, f"{pair}-name-diff.txt")
    req_diff_path  = os.path.join(output_dir, f"{pair}-req-diff.txt")

    key_data_diff(dict1, dict2, name_diff_path)
    data_requirements_diff(dict1, dict2, req_diff_path)
    print(f"  Diff files: {name_diff_path}, {req_diff_path}")

    # Task 3 - map to Kubescape controls
    print("[Task 3] Mapping differences to Kubescape controls...")
    content1, content2 = task_three_input_function(name_diff_path, req_diff_path)
    controls_path = os.path.join(output_dir, f"{pair}-controls.txt")
    controls = identify_kubescape_controls(content1, content2, controls_path)
    print(f"  Controls: {controls if controls else 'NO DIFFERENCES FOUND'}")

    # Task 3 - run Kubescape and generate CSV
    if os.path.exists(YAMLS_ZIP):
        print("[Task 3] Running Kubescape scan...")
        try:
            df = execute_kubescape(controls_path, YAMLS_ZIP, output_dir=output_dir)
            csv_path = os.path.join(output_dir, f"{pair}-results.csv")
            generate_csv(df, csv_path)
            print(f"  CSV results: {csv_path}")
        except Exception as e:
            print(f"  Kubescape error: {e}")
    else:
        print(f"  Skipping Kubescape scan ({YAMLS_ZIP} not found)")

    print(f"  Done: {pair}")


def main():
    if len(sys.argv) == 3:
        run_pipeline(sys.argv[1], sys.argv[2])
    else:
        for file1, file2 in NINE_INPUTS:
            run_pipeline(file1, file2)


if __name__ == "__main__":
    main()
