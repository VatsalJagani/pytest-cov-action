import os
import sys

sys.path.append(os.path.dirname(__file__))

import github_action_toolkit as gat
from github_action_toolkit import JobSummary
import pytest_results_handler
import pytest_cov_report_handler


def main():
    print("Hello from pytest-cov-action!")
    gat.print_all_user_inputs()

    pytest_results_file = gat.get_user_input('pytest_results_file')

    pytest_cov_file = gat.get_user_input('pytest_cov_file')
    pytest_cov_file = None if pytest_cov_file == "NONE" else pytest_cov_file

    # pytest_results_add_to_job_summary = gat.get_user_input_as('pytest_results_add_to_job_summary', bool, True)
    # pytest_cov_add_to_job_summary = gat.get_user_input_as('pytest_cov_add_to_job_summary', bool, True)
    pytest_cov_failure_threshold = gat.get_user_input_as('pytest_cov_failure_threshold', float, 0.0)
    show_passing_test_cases = gat.get_user_input_as('show_passing_test_cases', bool, False)

    # Pytest Results
    pytest_result = pytest_results_handler.parse_pytest_xml(pytest_results_file)

    is_pytest_passed = True if pytest_result['failed_tests'] == 0 and pytest_result['errors'] == 0 else False
    print(f"is_pytest_passed = {is_pytest_passed}")

    pytest_summary = JobSummary()
    pytest_results_handler.generate_summary(pytest_result, pytest_summary, show_passing_test_cases)
    pytest_summary.write()

    # Pytest Coverage Report
    if pytest_cov_file:
        pytest_cov_result = pytest_cov_report_handler.parse_coverage_xml(pytest_cov_file)
        pytest_cov = pytest_cov_result["coverage_percentage"]
        print(f"pytest_overall_cov = {pytest_cov} %")
        pytest_cov_summary = JobSummary()
        pytest_cov_report_handler.generate_summary(pytest_cov_result, pytest_cov_summary)
        pytest_cov_summary.write()
    else:
        gat.warning("No pytest coverage report given.")

    if not is_pytest_passed or (pytest_cov_file and pytest_cov<pytest_cov_failure_threshold):
        sys.exit(5)

if __name__ == "__main__":
    main()
