import os
import sys
import logging
import traceback

import cipush
import cipush.parser as p 
from cipush.backend import librato_backend
from cipush.backend import json_backend
from cipush.ci import default
from cipush.ci import circle
from cipush.ci import travis
from cipush import conf

logger = logging.getLogger(__name__)

BACKEND_MAP = (
        ('json', json_backend.Backend()),
        ('librato',librato_backend.Backend())
    )

CI_MAP = (
        ('default', default.Ci()),
        ('circle', circle.Ci()),
        ('travis', travis.Ci()),
    )

def get_backend(slug):
    d = dict(BACKEND_MAP)
    try:
        return d[slug]
    except KeyError:
        raise cipush.CiPushException(
            'no backend available for slug: {slug} '
            '- backends supported: {backends}'.format(
                    slug=slug,
                    backends= ','.join(d.keys())
                ))

def get_ci(slug):
    d = dict(CI_MAP)
    try:
        return d[slug]
    except:
        raise cipush.CiPushException(
            'no CI available for slug: {slug} '
            '- CIs supported: {ci}'.format(
                    slug=slug,
                    ci= ','.join(d.keys())
                ))


def capture_metric(metrics_type, suite_slug, backend_slug, ci_slug, path_pattern):
    backend_instance = get_backend(backend_slug)
    ci_instance = get_ci(ci_slug)

    if metrics_type == 'junit':
        duration = p.aggregate_from_files(p.get_duration_from_junit_xml, path_pattern)
        num_tests = p.aggregate_from_files(p.get_num_tests_from_junit_xml, path_pattern) 
        backend_instance.add(metrics_type, suite_slug, ci_instance, 'duration', duration)
        backend_instance.add(metrics_type, suite_slug, ci_instance, 'num_tests', num_tests)

    elif metrics_type == 'coverage':
        coverage = p.coverage_from_path(path_pattern)
        backend_instance.add(metrics_type, suite_slug, ci_instance, 'coverage', coverage)


def submit(backend_slug, ci_slug):
    backend_instance = get_backend(backend_slug)
    ci_instance = get_ci(ci_slug)
    print ci_instance.get_project_name()
    print ci_instance.get_branch_name()
    print ci_instance.get_build_link()


    backend_instance.submit(ci_instance)    
    

def push(args):
    try:
        logger.debug('configuring')
        conf.configure_logging(args)
        config_list = conf.get_config_list(args)
        logger.info('configured')

        for single_conf_dict in config_list:
            metrics_type = 'junit' if 'junit' in single_conf_dict else 'coverage'
            d = single_conf_dict[metrics_type]

            logger.debug('capturing metric type %s, suite: %s, backend: %s, ci: %s, on path: %s ', metrics_type, d['suite'], d['backend'], d['ci'], d['pwd'])
            capture_metric(metrics_type, d['suite'], d['backend'], d['ci'], d['pwd'])
        
        logger.debug('submitting metrics on backend: %s on ci: %s', d['backend'], d['ci'])
        submit(d['backend'], d['ci'])
    except cipush.CiPushException as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.critical('%s\n%s', repr(e), traceback.format_exc())
        sys.exit(1)
