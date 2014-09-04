import json
import sys

import cipush.backend

class Backend(cipush.backend.BaseBackend):

    def submit(self):
        sys.stdout.write(json.dumps(self._queue, indent=2))
         