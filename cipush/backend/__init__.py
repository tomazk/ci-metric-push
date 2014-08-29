class BaseBackend(object):

    metric_format = '{metrics_type}.{project_name}.{suite_slug}.{branch}.{metric}'
    
    def push(self):
        pass