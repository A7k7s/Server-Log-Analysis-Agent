# tools/semantic_grouping.py

from difflib import SequenceMatcher

def group_errors_py(errors, similarity_threshold=0.6):
    clusters = []

    for err in errors:
        added = False
        for cluster in clusters:
            if any(SequenceMatcher(None, err, c).ratio() > similarity_threshold for c in cluster):
                cluster.append(err)
                added = True
                break
        if not added:
            clusters.append([err])
    return clusters
