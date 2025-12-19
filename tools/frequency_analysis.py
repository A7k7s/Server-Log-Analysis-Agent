# tools/frequency_analysis.py

import pandas as pd

def analyze_frequency_py(errors, timestamps):
    df = pd.DataFrame({"timestamp": timestamps, "error": errors})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    freq_stats = df.groupby("error").size().sort_values(ascending=False)
    return freq_stats
