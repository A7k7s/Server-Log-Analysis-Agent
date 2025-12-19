# main.py

import os
from agents.log_preprocessor import preprocess_logs
from agents.log_analysis_agent import LogAnalysisAgent
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def main():
    log_file_path = r""  # Replace with your path
    if not os.path.exists(log_file_path):
        print(f"[ERROR] Log file not found: {log_file_path}")
        return

    log_chunks = preprocess_logs(log_file_path)
    print(f"[INFO] Total chunks: {len(log_chunks)}")

    client = Groq(api_key=GROQ_API_KEY)
    agent = LogAnalysisAgent(client)
    final_report = agent.run(log_chunks)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/final_report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)

    print("[SUCCESS] Analysis completed")
    print(f"[INFO] Text report saved to outputs/final_report.txt")
    print(f"[INFO] PDF report saved to outputs/final_report.pdf")

if __name__ == "__main__":
    main()
