import json
import sys

import cipush.backend

class Backend(cipush.backend.BaseBackend):

    def push(self, metrics_type, suite_slug, ci_instance, metrics_dict):
        metrics = []
        for metric_name, value in metrics_dict.iteritems():
            metrics.append({
                'metric': self.metric_format.format(
                        metrics_type=metrics_type,
                        project_name=ci_instance.get_project_name(),
                        suite_slug=suite_slug,
                        branch=ci_instance.get_branch_name(),
                        metric=metric_name
                    ),
                'value': value
            })
        sys.stdout.write(json.dumps(metrics, indent=2))
         