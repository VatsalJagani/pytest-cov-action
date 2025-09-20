import os
import sys

sys.path.append(os.path.dirname(__file__))

import github_action_toolkit as gat
import pytest_results_handler
import pytest_cov_report_handler


if __name__ == "__main__":
    gat.debug("Running Python script main.py")

    gat.print_all_user_inputs()

    pytest_results_file = gat.get_user_input('pytest_results_file')

    pytest_cov_file = gat.get_user_input('pytest_cov_file')
    pytest_cov_file = None if pytest_cov_file == "NONE" else pytest_cov_file

    pytest_results_add_to_job_summary = gat.get_user_input_as('pytest_results_add_to_job_summary', bool, True)
    pytest_cov_add_to_job_summary = gat.get_user_input_as('pytest_cov_add_to_job_summary', bool, True)
    pytest_cov_failure_threshold = gat.get_user_input_as('pytest_cov_failure_threshold', float, 0.0)
    show_passing_test_cases = gat.get_user_input_as('show_passing_test_cases', bool, False)


    # Pytest Results
    is_pytest_passed = pytest_results_handler.is_passed(pytest_results_file)
    print(f"is_pytest_passed = {is_pytest_passed}")
    pytest_results_job_summary = pytest_results_handler.generate_md_summary(pytest_results_file, show_passing_test_cases=show_passing_test_cases)
    gat.append_job_summary(pytest_results_job_summary)

    # Pytest Coverage Report
    if pytest_cov_file:
        pytest_cov = pytest_cov_report_handler.get_overall_cov(pytest_cov_file)
        print(f"pytest_overall_cov = {pytest_cov} %")
        pytest_cov_job_summary = pytest_cov_report_handler.generate_md_summary(pytest_cov_file)
        gat.append_job_summary(pytest_cov_job_summary)
    else:
        gat.warning("No pytest coverage report given.")

    if not is_pytest_passed or (pytest_cov_file and pytest_cov<pytest_cov_failure_threshold):
        sys.exit(5)
