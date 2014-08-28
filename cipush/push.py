import os
import cipush.parser as p 

def get_backend_class(backend_slug):
    '''
    we're expecting that backend module has backend.Backend class
    '''
    import imp
    backend = imp.load_source(
        'cipush.backend.{0}'.format(backend_slug), 
        os.path.join(os.path.dirname(__file__),'backend', '{0}.py'.format(backend_slug))
        )
    return backend.Backend


def push(metrics_type, backend_slug, path_pattern):
    #Backend = get_backend_class(backend_slug)
    if metrics_type == 'junit':
        duration = p.aggregate_from_files(p.get_duration_from_junit_xml, path_pattern)
        num_tests = p.aggregate_from_files(p.get_num_tests_from_junit_xml, path_pattern) 
    elif metrics_type == 'coverage':
        coverage = p.coverage_from_path(path_pattern)
        coverage *= 100.
    print vars()

