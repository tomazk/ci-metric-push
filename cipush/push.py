import os
import cipush.parser as p 

def get_module(typ, slug):
    '''import imp # we're importing here since we'll have to cover python 3.4 also
    module = imp.load_source(
        'cipush.{0}.{1}'.format(typ,slug), 
        os.path.join(os.path.dirname(__file__),typ, '{0}.py'.format(slug))
        )'''
    print 'cipush.{0}.{1}'.format(typ,slug)
    module = __import__('cipush.{0}.{1}'.format(typ,slug)) 
    print module
    return module


def push(metrics_type, suite_slug, backend_slug, ci_slug, path_pattern):
    backend_module = get_module('backend', backend_slug)
    ci_module = get_module('ci', ci_slug)


    metrics_dict = {}
    if metrics_type == 'junit':
        metrics_dict['duration'] = p.aggregate_from_files(p.get_duration_from_junit_xml, path_pattern)
        metrics_dict['num_tests'] = p.aggregate_from_files(p.get_num_tests_from_junit_xml, path_pattern) 
        
    elif metrics_type == 'coverage':
        metrics_dict['coverage'] = p.coverage_from_path(path_pattern)

    print metrics_dict

    backend_module.push(metrics_type, suite_slug, ci_module, metrics_dict)
    

