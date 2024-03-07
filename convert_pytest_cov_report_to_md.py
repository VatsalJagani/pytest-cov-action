import xml.etree.ElementTree as ET
import sys

def parse_coverage_xml(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    summary = {
        'total_lines': 0,
        'covered_lines': 0,
        'coverage_percentage': 0,
        'packages': []
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
        package_data = {
            'name': package.get('name'),
            'total_lines': 0,
            'covered_lines': 0,
            'coverage_percentage': 0,
            'files': []
        }

        for source_file in package.iter('class'):
            file_data = {
                'name': source_file.get('name'),
                'total_lines': 0,
                'covered_lines': 0,
                'coverage_percentage': 0
            }

            total_lines = source_file.get('lines-valid')
            if total_lines is not None:
                file_data['total_lines'] = int(total_lines)

            covered_lines = source_file.get('lines-covered')
            if covered_lines is not None:
                file_data['covered_lines'] = int(covered_lines)

            coverage_percentage = source_file.get('line-rate')
            if coverage_percentage is not None:
                file_data['coverage_percentage'] = float(coverage_percentage) * 100

            package_data['files'].append(file_data)

        total_lines = package.get('lines-valid')
        if total_lines is not None:
            package_data['total_lines'] = int(total_lines)

        covered_lines = package.get('lines-covered')
        if covered_lines is not None:
            package_data['covered_lines'] = int(covered_lines)

        coverage_percentage = package.get('line-rate')
        if coverage_percentage is not None:
            package_data['coverage_percentage'] = float(coverage_percentage) * 100

        

        summary['packages'].append(package_data)

    return summary


def generate_readme(summary):
    readme = f"# Pytest Coverage Summary\n\n"
    readme += f"Total Lines: {summary['total_lines']}\n"
    readme += f"Covered Lines: {summary['covered_lines']}\n"
    readme += f"Coverage Percentage: {summary['coverage_percentage']:.2f}%\n\n"

    readme += "## Packages\n\n"
    readme += "| Package | File | Total Lines | Covered Lines | Coverage Percentage |\n"
    readme += "|---------|-------------|-------------|---------------|----------------------|\n"
    for package in summary['packages']:
        for source_file in package['files']:
            readme += f"| {package['name']} | {source_file['name']} | {source_file['total_lines']} | {source_file['covered_lines']} | {source_file['coverage_percentage']:.2f}% |\n"

    return readme


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python coverage_summary.py <path_to_xml_file>")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    summary = parse_coverage_xml(xml_file_path)
    readme_content = generate_readme(summary)

    with open('coverage_summary.md', 'w') as readme_file:
        readme_file.write(readme_content)

    print(f"Summary written to 'coverage_summary.md'")
