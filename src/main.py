import os
import sys

sys.path.append(os.path.dirname(__file__))

import helpers.github_action_utils as utils
import pytest_results_handler
import pytest_cov_report_handler



if __name__ == "__main__":
    utils.info("Running Python script main.py")

    pytest_results_file = utils.get_input('pytest_results_file')
    utils.info("pytest_results_file: {}".format(pytest_results_file))

    pytest_cov_file = utils.get_input('pytest_cov_file')
    pytest_cov_file = None if pytest_cov_file == "NONE" else pytest_cov_file
    utils.info("pytest_cov_file: {}".format(pytest_cov_file))

    pytest_results_add_to_job_summary = utils.str_to_boolean_default_true(
        utils.get_input('pytest_results_add_to_job_summary'))
    utils.info("pytest_results_add_to_job_summary: {}".format(pytest_results_add_to_job_summary))

    pytest_cov_add_to_job_summary = utils.str_to_boolean_default_true(
        utils.get_input('pytest_cov_add_to_job_summary'))
    utils.info("pytest_cov_add_to_job_summary: {}".format(pytest_cov_add_to_job_summary))

    pytest_cov_failure_threshold = float(utils.get_input('pytest_cov_failure_threshold'))
    utils.info("pytest_cov_failure_threshold: {}".format(pytest_cov_failure_threshold))


    # Pytest Results
    is_pytest_passed = pytest_results_handler.is_passed(pytest_results_file)
    print(f"is_pytest_passed = {is_pytest_passed}")
    pytest_results_job_summary = pytest_results_handler.generate_md_summary(pytest_results_file)
    utils.write_msg_to_step_summary(pytest_results_job_summary)

    # Pytest Coverage Report
    if pytest_cov_file:
        pytest_cov = pytest_cov_report_handler.get_overall_cov(pytest_cov_file)
        print(f"pytest_overall_cov = {pytest_cov} %")
        pytest_cov_job_summary = pytest_cov_report_handler.generate_md_summary(pytest_cov_file)
        utils.write_msg_to_step_summary(pytest_cov_job_summary)
    else:
        utils.info("No pytest coverage report given.")

    if not is_pytest_passed or (pytest_cov_file and pytest_cov<pytest_cov_failure_threshold):
        sys.exit(5)
