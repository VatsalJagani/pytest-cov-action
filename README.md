# pytest-cov-action
GitHub Action to add for Pytest and Pytest Coverage Report in GitHub Action Summary.


## Capabilities & Usage

* You can get more information about GitHub workflow files [here](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions). As this document will not go in detail about it.

* Example-1
    ```
    - uses: VatsalJagani/pytest-cov-action@v0.4
      with:
        pytest_results_file: "junit/test-results.xml"
        pytest_cov_file: "junit/coverage.xml"
      if: ${{ always() }}
    ```

* Example-2 - Coverage report is optional
    ```
    - uses: VatsalJagani/pytest-cov-action@v0.4
      with:
        pytest_results_file: "test-results.xml"
      if: ${{ always() }}
    ```

* Screenshot - Pytest-cases Passing
    * ![Pytests Passing](/images/pytest_passing.png)

* Screenshot - Pytest-cases Failing
    * ![Pytests Failing](/images/pytest_failing.png)



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


## Troubleshooting
* GitHub action failing even though all test-cases are passing.
    * **Issue** - It could be most likely due to default value of `pytest_cov_failure_threshold` is `70%`. If your test-coverage is lower than that, it would fail the GitHub action.
    * **Solution** - If you don't care about pytest-coverage you can change the input `pytest_cov_failure_threshold` to `0` in order to avoid this error.
        ```
        - uses: VatsalJagani/pytest-cov-action@v0.4
          with:
            pytest_results_file: "junit/test-results.xml"
            pytest_cov_file: "junit/coverage.xml"
            pytest_cov_failure_threshold: 0
          if: ${{ always() }}
        ```

* There are no summaries being added on GitHub action step
    * **Issue** - No summaries being added to GitHub action's summary even though test-cases are being executed properly.
    * **Solution** - If test-cases are failing and you forgot to add `if: ${{ always() }}` in actions' parameter, the action would not be executed because some test have failed. So add it like:
        ```
        - uses: VatsalJagani/pytest-cov-action@v0.4
          with:
            pytest_results_file: "junit/test-results.xml"
            pytest_cov_file: "junit/coverage.xml"
          if: ${{ always() }}
        ```



## Release Notes

### v1
* First version of the GitHub action with use-case of adding Pytest-report and Pytest-cov-report to GitHub action step summary.
