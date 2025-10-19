import xml.etree.ElementTree as ET
import sys
from github_action_toolkit import JobSummary

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


def generate_summary(coverage_data, summary: JobSummary):
    summary.add_heading("Pytest Coverage Summary", 1)
    summary.add_list([
        f"Total Lines: {coverage_data['total_lines']}",
        f"Covered Lines: {coverage_data['covered_lines']}",
        f"Coverage Percentage: {coverage_data['coverage_percentage']:.2f}%"
    ])

    summary.add_break()

    # Create table data
    table_data = [["Package", "File", "Total Lines", "Covered Lines", "Coverage Percentage"]]
    
    for package_name in coverage_data['packages']:
        # Add package row
        table_data.append([
            f"<b>{package_name}</b>",
            "",
            f"<b>{coverage_data['packages'][package_name]['total_lines']}</b>",
            f"<b>{coverage_data['packages'][package_name]['covered_lines']}</b>",
            f"<b>{coverage_data['packages'][package_name]['coverage_percentage']:.2f}%</b>"
        ])
        
        # Add file rows
        for file_name in coverage_data['packages'][package_name]['files']:
            table_data.append([
                "",
                file_name,
                str(coverage_data['packages'][package_name]['files'][file_name]['total_lines']),
                str(coverage_data['packages'][package_name]['files'][file_name]['covered_lines']),
                f"{coverage_data['packages'][package_name]['files'][file_name]['coverage_percentage']:.2f}%"
            ])
    
    summary.add_table(table_data)
    return summary
