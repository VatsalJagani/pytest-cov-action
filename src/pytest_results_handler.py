import xml.etree.ElementTree as ET
from github_action_toolkit import JobSummary


def parse_pytest_xml(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    result = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'skipped_tests': 0,
        'errors': 0,
        'total_time': 0,
        'test_cases': []
    }

    for testcase in root.iter('testcase'):
        result['total_tests'] += 1
        test_case = {
            'name': testcase.get('classname') + '.' + testcase.get('name'),
            'result': 'passed',
            'duration': float(testcase.get('time'))
        }

        result['total_time'] += test_case['duration']

        failure = testcase.find('failure')
        error = testcase.find('error')
        if failure is not None:
            result['failed_tests'] += 1
            test_case['result'] = 'failed'
            test_case['failure_message'] = failure.get('message')
            test_case['failure_traceback'] = failure.text.strip()
        elif error is not None:
            result['errors'] += 1
            test_case['result'] = 'error'
            test_case['error_message'] = error.get('message')
            test_case['error_traceback'] = error.text.strip()

        result['test_cases'].append(test_case)

    result['passed_tests'] = result['total_tests'] - result['failed_tests'] - result['errors']
    result['skipped_tests'] = len(list(root.iter('skipped')))

    return result


def generate_summary(pytest_result, summary: JobSummary, show_passing_test_cases=False):
    summary.add_heading("Pytest Summary", 1)
    summary.add_list([
        f":information_source: Total Tests: {pytest_result['total_tests']}",
        f":white_check_mark: Passed Tests: {pytest_result['passed_tests']}",
        f":x: Failed Tests: {pytest_result['failed_tests']}",
        f":x: Errors: {pytest_result['errors']}",
        f":heavy_exclamation_mark: Skipped Tests: {pytest_result['skipped_tests']}",
        f":clock1130: Total Time: {pytest_result['total_time']:.2f} seconds"
    ])

    summary.add_break()

    if show_passing_test_cases:
        summary.add_heading("Passed Test-Cases", 3)

        summary.add_table([
            ["Test-Case", "Duration (sec)"],
            *[
                [test_case['name'], f"{test_case['duration']:.2f}"]
                for test_case in pytest_result['test_cases']
                if test_case['result'].lower() == "passed"
            ]
        ])
        summary.add_break()

    if float(pytest_result['failed_tests']) + float(pytest_result['errors']) + float(pytest_result['skipped_tests']) > 0:

        summary.add_heading("Failed/Test-Cases", 2)

        summary.add_table([
            ["Test-Case", "Result", "Duration (sec)", "Details"],
            *[
                [
                    test_case['name'],
                    test_case['result'].capitalize(),
                    f"{test_case['duration']:.2f}",
                    f"```\n{test_case['failure_traceback'] if test_case['result']=='failed' else test_case['error_traceback']}\n```"
                ]
                for test_case in pytest_result['test_cases']
                if test_case['result'].lower() in ["failed", "error"]
            ]
        ])

        summary.add_break()

    return summary
