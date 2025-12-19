# tools/executive_summary.py

from fpdf import FPDF
import os

def generate_summary(grouped_errors, freq_stats, client):
    grouped_text = "\n\n".join([f"Cluster {i+1}:\n" + "\n".join(cluster) 
                                for i, cluster in enumerate(grouped_errors)])

    prompt = (
        "You are a server log analysis expert. "
        "Write an executive summary report combining impact analysis "
        "for the following error clusters and their frequencies:\n\n"
        f"{grouped_text}\n\n"
        f"Top Frequencies:\n{freq_stats.head(10)}"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You generate executive summary reports."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def save_report_as_pdf(text, filename="outputs/final_report.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(filename)
    print(f"[INFO] PDF saved to {filename}")
