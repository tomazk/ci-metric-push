import json
import sys

import cipush.backend

class Backend(cipush.backend.BaseBackend):

    def submit(self, *args, **kwargs):
        l = []
        for metric_name, metric_value in self._queue:
            l.append({metric_name: metric_value})
        sys.stdout.write(json.dumps(l, indent=2))
         