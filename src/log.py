import json
from datetime import datetime

def log_dict(dict):
    print(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                **dict
            },
            indent=2
        ))
