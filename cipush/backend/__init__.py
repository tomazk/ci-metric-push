import logging

logger = logging.getLogger(__name__)

class BaseBackend(object):

    metric_format = '{metrics_type}.{project_name}.{suite_slug}.{branch}.{metric_slug}'
    
    def __init__(self):
        self._queue = [] 

    def add(self, metrics_type, suite_slug, ci_instance, metric_slug, metric_value):
        metric_name = self.metric_format.format(
                metrics_type=metrics_type,
                project_name=ci_instance.get_project_name(),
                suite_slug=suite_slug,
                branch=ci_instance.get_branch_name(),
                metric_slug=metric_slug
            )
        self._queue.append((metric_name, metric_value))
        logger.debug('captured metric %s: %s', metric_name, str(metric_value))
