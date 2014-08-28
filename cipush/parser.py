
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

