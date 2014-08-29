import os

import cipush.parser as p 
from cipush.backend import librato
from cipush.backend import json_backend
from cipush.ci import default

BACKEND_MAP = (
        ('json', json_backend.Backend),
    )

CI_MAP = (
        ('default', default.Ci),
    )

def get_backend(slug):
    d = dict(BACKEND_MAP)
    return d[slug]

def get_ci(slug):
    d = dict(CI_MAP)
    return d[slug]


def push(metrics_type, suite_slug, backend_slug, ci_slug, path_pattern):
    backend_instance = get_backend(backend_slug)()
    ci_instance = get_ci(ci_slug)()

    metrics_dict = {}
    if metrics_type == 'junit':
        metrics_dict['duration'] = p.aggregate_from_files(p.get_duration_from_junit_xml, path_pattern)
        metrics_dict['num_tests'] = p.aggregate_from_files(p.get_num_tests_from_junit_xml, path_pattern) 
        
    elif metrics_type == 'coverage':
        metrics_dict['coverage'] = p.coverage_from_path(path_pattern)

    backend_instance.push(metrics_type, suite_slug, ci_instance, metrics_dict)
    

