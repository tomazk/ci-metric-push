import os
import cipush.parser as p 

def get_class(typ, slug):
    '''
    we're expecting that backend module has backend.Backend class
    '''
    import imp
    backend = imp.load_source(
        'cipush.{0}.{1}'.format(typ,slug), 
        os.path.join(os.path.dirname(__file__),typ, '{0}.py'.format(slug))
        )
    return backend.Backend


def push(metrics_type, backend_slug, ci_slug, path_pattern):
    BackendClass = get_class('backend', backend_slug)
    CiClass = get_class('ci', ci_slug)

    if metrics_type == 'junit':
        duration = p.aggregate_from_files(p.get_duration_from_junit_xml, path_pattern)
        num_tests = p.aggregate_from_files(p.get_num_tests_from_junit_xml, path_pattern) 
        
    elif metrics_type == 'coverage':
        coverage = p.coverage_from_path(path_pattern)
    

