# pytest-cov-action
GitHub Action to add for Pytest and Pytest Coverage Report in GitHub Action Summary.


## Capabilities & Usage

* You can get more information about GitHub workflow files [here](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions). As this document will not go in detail about it.

* Example-1
    ```
    - uses: VatsalJagani/pytest-cov-action@v0.1
      with:
        pytest_results_file: "junit/test-results.xml"
        pytest_cov_file: "junit/coverage.xml"
    ```

* Example-2 - Coverage report is optional
    ```
    - uses: VatsalJagani/pytest-cov-action@v0.1
      with:
        pytest_results_file: "test-results.xml"
    ```



## Inputs

#### pytest_results_file:
* description: "Path for pytest results file. This has to be a pytest results file in XML format."
* required: true

#### pytest_cov_file:
* description: "Path for pytest-coverage report file. This has to be a pytest coverage report file in XML format."
* required: false
* default: "NONE"

#### pytest_results_add_to_job_summary:
* description: "Add pytest results to GitHub Action's Job Summary"
* required: false
* default: true

### pytest_cov_add_to_job_summary:
* description: "Add pytest-coverage report to GitHub Action's Job Summary"
* required: false
* default: true

### pytest_cov_failure_threshold:
* description: "Fail the coverage report if coverage percentage is below this threshold."
* required: false
* default: 70

### show_passing_test_cases:
* description: "Enable this input parameter if you wish to show list of all test-cases which has passed."
* required: false
* default: false



## See Examples Here
* [Public GitHub Repository using this Action](https://github.com/VatsalJagani/pytest-cov-action/network/dependents)


## Release Notes

### v1
* First version of the GitHub action with use-case of adding Pytest-report and Pytest-cov-report to GitHub action step summary.
