import json
import os
from datetime import datetime

_is_stdout = False

_LOGFILE_PATH = os.path.expanduser("~/.cache/nlcontrols/logs.txt")

def log_dict(dict):
    content = json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                **dict
            },
            indent=2
        )
    if _is_stdout:
        print(content)
    with open(_LOGFILE_PATH, "a") as f:
        f.write(content)

def set_stdout(val: bool):
    global _is_stdout
    _is_stdout = val
