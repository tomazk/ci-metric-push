import os
import cipush.backend

def connect_to_librato():
    import librato
    try:
        librato_user = os.environ['LIBRATO_USER']
        librato_token = os.environ['LIBRATO_TOKEN']
    except KeyError:
        raise Exception('librato user or token not set in enviroment settings ' +
        'LIBRATO_USER and LIBRATO_TOKEN despite set COVERAGE_ENABLED enviroment variable')

    return librato.connect(librato_user, librato_token)

'''
def post_tests_metrics_to_librato(librato_api, coverage_percentage, num_of_tests, tests_elapsed_time):

    queue = librato_api.new_queue()
    queue.add('tests.{0}.coverage_percentage'.format(settings.PROJECT_NAME), coverage_percentage ,type='gauge', source='circle-ci')
    queue.add('tests.{0}.num_of_tests'.format(settings.PROJECT_NAME), num_of_tests ,type='gauge', source='circle-ci')
    queue.add('tests.{0}.tests_elapsed_time'.format(settings.PROJECT_NAME), tests_elapsed_time ,type='gauge', source='circle-ci')
    queue.submit()

    circleci_link = 'https://circleci.com/gh/{0}/{1}/{2}'.format(
            os.environ.get('CIRCLE_PROJECT_USERNAME'),
            os.environ.get('CIRCLE_PROJECT_REPONAME'),
            os.environ.get('CIRCLE_BUILD_NUM'),
        )
    librato_api.post_annotation('circle_ci.{0}'.format(settings.PROJECT_NAME),
        title='build triggered by {0}'.format(os.environ.get('CIRCLE_USERNAME')), 
        source='circle-ci', 
        description=circleci_link,
        links=[{'rel': 'circleci', 'href': circleci_link, 'label': circleci_link}]       
        )
'''


class Backend(cipush.backend.BaseBackend):

    def push(self, metrics_type, suite_slug, ci_instance, metrics_dict):
        librato_api = connect_to_librato()

        # post metrics
        queue = librato_api.new_queue()
        for metric_name, value in metrics_dict.iteritems():
            librato_metric_name = self.metric_format.format(
                    metrics_type=metrics_type,
                    project_name=ci_instance.get_project_name(),
                    suite_slug=suite_slug,
                    branch=ci_instance.get_branch_name(),
                    metric=metric_name
                )
            queue.add(librato_metric_name, value, type='gauge', source='circle-ci')
        queue.submit()

        # post annotation
        librato_annotation_name = 'circle_ci.{0}.{1}'.format(
                metrics_type,
                ci_instance.get_project_name()
            )
        librato_api.post_annotation(librato_annotation_name,
                title='build triggered by {0}'.format(ci_instance.get_user_name()), 
                source='circle-ci', 
                description=ci_instance.get_build_link(),
                links=[{'rel': 'circleci', 'href': ci_instance.get_build_link()}]       
            )
