import os
import logging

import cipush.backend

logger = logging.getLogger(__name__)

def connect_to_librato():
    import librato
    try:
        librato_user = os.environ['LIBRATO_USER']
        librato_token = os.environ['LIBRATO_TOKEN']
    except KeyError:
        raise Exception('librato user or token not set in enviroment settings ' +
        'LIBRATO_USER and LIBRATO_TOKEN despite set COVERAGE_ENABLED enviroment variable')

    return librato.connect(librato_user, librato_token)

def post_librato_annotation(librato_api, ci_instance):    
    librato_annotation_name = 'build_annotation.{project_name}.{branch}'.format(
            project_name=ci_instance.get_project_name(),
            branch=ci_instance.get_branch_name(),
        )
    librato_api.post_annotation(librato_annotation_name,
            title='build triggered by {0}'.format(ci_instance.get_user_name()), 
            source='circle-ci', 
            description=ci_instance.get_build_link(),
            links=[{'rel': 'circleci', 'href': ci_instance.get_build_link()}]       
        )


class Backend(cipush.backend.BaseBackend):

    def submit(self, ci_instance=None):

        librato_api = connect_to_librato()
        logger.debug('connected to librato using env variables LIBRATO_USER and LIBRATO_TOKEN')

        queue = librato_api.new_queue()
        for metric_name, value in self._queue:
            queue.add(metric_name, value, type='gauge', source='circle-ci')
        queue.submit()
        logger.debug('submitted metrics to librato')

        if ci_instance:
           post_librato_annotation(librato_api, ci_instance)
           logger.debug('posted build annotation to librato')


