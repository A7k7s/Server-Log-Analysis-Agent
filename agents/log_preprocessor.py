# agents/log_preprocessor.py

import os

def preprocess_logs(log_file_path, chunk_size=1000):
    """
    Reads a log file, cleans it, and splits into chunks.
    Returns a list of log chunks.
    """
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    with open(log_file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Remove empty lines and strip whitespace
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Split into chunks
    chunks = [
        cleaned_lines[i:i + chunk_size]
        for i in range(0, len(cleaned_lines), chunk_size)
    ]

    return chunks
