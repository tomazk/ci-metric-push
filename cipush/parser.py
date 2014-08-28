import glob
from xml.etree import ElementTree as et


def get_coverage_from_cobertura_xml(tree):
    root = tree.getroot()
    assert root.tag == 'coverage'
    return float(root.attrib['line-rate'])

def get_num_tests_from_junit_xml(tree):
    root = tree.getroot()
    if root.tag == 'testsuite':
        return int(root.attrib['tests'])

    num_tests = 0
    for el in root.findall('testsuite'):
        num_tests += int(el.attrib['tests'])
    return num_tests

def get_duration_from_junit_xml(tree):
    root = tree.getroot()
    if root.tag == 'testsuite':
        return float(root.attrib['time'])

    duration = 0.
    for el in root.findall('testsuite'):
        duration += float(el.attrib['time'])
    return duration


def aggregate_from_files(aggregate_function, path_pattern):
    return sum(aggregate_function(et.parse(p)) for p in glob.glob(path_pattern))

def coverage_from_path(path_pattern):
    files = glob.glob(path_pattern)
    file_, = files
    return get_coverage_from_cobertura_xml(et.parse(file_))

