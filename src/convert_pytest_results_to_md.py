import xml.etree.ElementTree as ET
import sys

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

    readme += "## Test Cases\n\n"
    for test_case in summary['test_cases']:
        readme += f"### {test_case['name']}\n"
        readme += f"Result: {test_case['result'].capitalize()}\n"
        readme += f"Duration: {test_case['duration']:.2f} seconds\n"

        if test_case['result'] == 'failed':
            readme += f"Failure Message: {test_case['failure_message']}\n"
            readme += f"Failure Traceback:\n```\n{test_case['failure_traceback']}\n```\n"
        elif test_case['result'] == 'error':
            readme += f"Error Message: {test_case['error_message']}\n"
            readme += f"Error Traceback:\n```\n{test_case['error_traceback']}\n```\n"

        readme += "\n"

    return readme

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pytest_summary.py <path_to_xml_file>")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    summary = parse_pytest_xml(xml_file_path)
    readme_content = generate_readme(summary)

    with open('pytest_summary.md', 'w') as readme_file:
        readme_file.write(readme_content)

    print(f"Summary written to 'pytest_summary.md'")