import json
import sys


def push(metrics_type, suite_slug, ci_module, metrics_dict):
    metrics = []
    mformat = '{metrics_type}.{project_name}.{suite_slug}.{branch}.{metric}'
    for metric_name, value in metrics_dict.iteritems():
        metrics.append({
            'metric': mformat.format(
                    metrics_type=metrics_type,
                    project_name=ci_module.get_project_name(),
                    suite_slug=suite_slug,
                    branch=ci_module.get_branch_name(),
                    metric=metric_name
                ),
            'value': value
        
        })

    sys.stdout.write(json.dumps(metrics))
     