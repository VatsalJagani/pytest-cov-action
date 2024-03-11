import xml.etree.ElementTree as ET
import sys

def parse_coverage_xml(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    summary = {
        'total_lines': 0,
        'covered_lines': 0,
        'coverage_percentage': 0,
        'packages': {}
    }

    total_lines = root.get('lines-valid')
    if total_lines is not None:
        summary['total_lines'] = int(total_lines)

    covered_lines = root.get('lines-covered')
    if covered_lines is not None:
        summary['covered_lines'] = int(covered_lines)

    coverage_percentage = root.get('line-rate')
    if coverage_percentage is not None:
        summary['coverage_percentage'] = float(coverage_percentage) * 100

    for package in root.iter('package'):
        package_name = package.attrib['name']

        if package_name not in summary['packages']:
            summary['packages'][package_name] = {
                "total_lines": 0,
                "covered_lines": 0
            }
        package_dict = summary['packages'][package_name]

        for source_file in package.iter('class'):
            if 'files' not in package_dict:
                package_dict['files'] = {}

            file_name = source_file.attrib['filename']
            if file_name not in package_dict['files']:
                package_dict['files'][file_name] = {
                    "total_lines": 0,
                    "covered_lines": 0
                }
            file_dict = package_dict['files'][file_name]

            for line in source_file.iter('line'):
                line_number = int(line.attrib['number'])
                hits = int(line.attrib['hits'])

                file_dict['total_lines'] += 1
                package_dict['total_lines'] += 1

                if hits > 0:
                    file_dict['covered_lines'] += 1
                    package_dict['covered_lines'] += 1


    for package in summary['packages']:
        summary['packages'][package]['coverage_percentage'] = \
            float(summary['packages'][package]['covered_lines'] / summary['packages'][package]['total_lines']) * 100
    
        for source_file in summary['packages'][package]['files']:
            summary['packages'][package]['files'][source_file]['coverage_percentage'] = \
                float(summary['packages'][package]['files'][source_file]['covered_lines'] / summary['packages'][package]['files'][source_file]['total_lines']) * 100

    return summary


def generate_readme(summary):
    readme = f"# Pytest Coverage Summary\n\n"
    readme += f"Total Lines: {summary['total_lines']}\n"
    readme += f"Covered Lines: {summary['covered_lines']}\n"
    readme += f"Coverage Percentage: {summary['coverage_percentage']:.2f}%\n\n"

    readme += "\n\n"
    readme += "| Package | File | Total Lines | Covered Lines | Coverage Percentage |\n"
    readme += "|:---------|:-------------|-------------:|---------------:|----------------------:|\n"
    for package_name in summary['packages']:
        _escaped_package_name = package_name.replace('_', '\\_')
        readme += f"| **{_escaped_package_name}** | | "\
            f"**{summary['packages'][package_name]['total_lines']}** | **{summary['packages'][package_name]['covered_lines']}** | "\
            f"**{summary['packages'][package_name]['coverage_percentage']:.2f}%** |\n"

        for file_name in summary['packages'][package_name]['files']:
            _escaped_file_name = file_name.replace('_', '\\_')
            readme += f"| | {_escaped_file_name} | "\
            f"{summary['packages'][package_name]['files'][file_name]['total_lines']} | {summary['packages'][package_name]['files'][file_name]['covered_lines']} | "\
            f"{summary['packages'][package_name]['files'][file_name]['coverage_percentage']:.2f}% |\n"

    return readme


def get_overall_cov(pytest_cov_report_file):
    summary = parse_coverage_xml(pytest_cov_report_file)
    return summary['coverage_percentage']

def generate_md_summary(pytest_cov_report_file):
    summary = parse_coverage_xml(pytest_cov_report_file)
    return generate_readme(summary)