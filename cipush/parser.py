import glob
from xml.etree import ElementTree as et

import cipush

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
    files = glob.glob(path_pattern)
    if len(files) == 0:
        raise cipush.CiPushException('no junit xml files matched with pattern: {0}'.format(path_pattern))
    return sum(aggregate_function(et.parse(p)) for p in files)

def coverage_from_path(path_pattern):
    files = glob.glob(path_pattern)
    if len(files) != 1:
        raise cipush.CiPushException(
            'coverage can only be extracted from a single cobertura '
            'formated xml file - current pattern:{0} '
            'matches more then one file'.format(path_pattern)
            )

    file_, = files
    return get_coverage_from_cobertura_xml(et.parse(file_))

