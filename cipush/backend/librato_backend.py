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
        librato_annotation_name = '{metrics_type}.{project_name}.{suite_slug}.{branch}'.format(
                metrics_type=metrics_type,
                project_name=ci_instance.get_project_name(),
                suite_slug=suite_slug,
                branch=ci_instance.get_branch_name(),
            )
        librato_api.post_annotation(librato_annotation_name,
                title='build triggered by {0}'.format(ci_instance.get_user_name()), 
                source='circle-ci', 
                description=ci_instance.get_build_link(),
                links=[{'rel': 'circleci', 'href': ci_instance.get_build_link()}]       
            )
