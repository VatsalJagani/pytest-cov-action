import xml.etree.ElementTree as ET


def parse_pytest_xml(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    summary = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'skipped_tests': 0,
        'errors': 0,
        'total_time': 0,
        'test_cases': []
    }

    for testcase in root.iter('testcase'):
        summary['total_tests'] += 1
        test_case = {
            'name': testcase.get('classname') + '.' + testcase.get('name'),
            'result': 'passed',
            'duration': float(testcase.get('time'))
        }

        summary['total_time'] += test_case['duration']

        failure = testcase.find('failure')
        error = testcase.find('error')
        if failure is not None:
            summary['failed_tests'] += 1
            test_case['result'] = 'failed'
            test_case['failure_message'] = failure.get('message')
            test_case['failure_traceback'] = failure.text.strip()
        elif error is not None:
            summary['errors'] += 1
            test_case['result'] = 'error'
            test_case['error_message'] = error.get('message')
            test_case['error_traceback'] = error.text.strip()

        summary['test_cases'].append(test_case)

    summary['passed_tests'] = summary['total_tests'] - summary['failed_tests'] - summary['errors']
    summary['skipped_tests'] = len(list(root.iter('skipped')))

    return summary

def generate_readme(summary):
    readme = f"# Pytest Summary\n\n"
    readme += f"Total Tests: {summary['total_tests']}\n"
    readme += f"Passed Tests: {summary['passed_tests']}\n"
    readme += f"Failed Tests: {summary['failed_tests']}\n"
    readme += f"Errors: {summary['errors']}\n"
    readme += f"Skipped Tests: {summary['skipped_tests']}\n"
    readme += f"Total Time: {summary['total_time']:.2f} seconds\n\n"

    readme += "#### Passed Test-Cases\n\n"

    readme += "| Test-Case | Duration (sec) |\n"
    readme += "|:---------|----------:|\n"
    for test_case in summary['test_cases']:
        if test_case['result'].lower() == "passed":
            readme += f"| {test_case['name']} | {test_case['duration']:.2f} |"


    readme += "#### Failed Test-Cases\n\n"

    for test_case in summary['test_cases']:

        if test_case['result'].lower() == "passed":
            continue

        readme += f"* {test_case['name']}\n"
        readme += f"\t* Result: {test_case['result'].capitalize()}\n"
        readme += f"\t* Duration: {test_case['duration']:.2f} seconds\n"

        if test_case['result'] == 'failed':
            readme += f"\t* Failure Message: {test_case['failure_message']}\n"
            readme += f"\t* Failure Traceback:\n```\n{test_case['failure_traceback']}\n```\n"
        elif test_case['result'] == 'error':
            readme += f"\t* Error Message: {test_case['error_message']}\n"
            readme += f"\t* Error Traceback:\n```\n{test_case['error_traceback']}\n```\n"

        readme += "\n"

    return readme


def generate_md_summary(pytest_results_file):
    summary = parse_pytest_xml(pytest_results_file)
    return generate_readme(summary)


def is_passed(pytest_results_file):
    summary = parse_pytest_xml(pytest_results_file)
    if summary['failed_tests'] == 0:
        return True
    return False
