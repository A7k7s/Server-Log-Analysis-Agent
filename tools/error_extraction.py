# tools/error_extraction.py

import re

def extract_errors_py(log_chunk):
    errors = []
    timestamps = []
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*-\s*(.*)')

    for line in log_chunk:
        match = pattern.search(line)
        if match:
            ts, msg = match.groups()
            timestamps.append(ts)
            errors.append(msg)
        else:
            errors.append(line)
            timestamps.append(None)
    return errors, timestamps
