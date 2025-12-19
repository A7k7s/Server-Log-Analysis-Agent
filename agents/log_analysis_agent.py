from tools.error_extraction import extract_errors_py
from tools.semantic_grouping import group_errors_py
from tools.frequency_analysis import analyze_frequency_py
from tools.executive_summary import generate_summary, save_report_as_pdf
from memory.agent_memory import AgentMemory


class LogAnalysisAgent:
    """
    Agentic hybrid:
    - Python tools: error extraction, semantic grouping, frequency
    - LLM decides which tool to call next dynamically
    - LLM generates final summary
    """

    def __init__(self, llm_client):
        self.client = llm_client
        self.memory = AgentMemory()
        self.available_tools = ["ErrorExtraction", "SemanticGrouping", "FrequencyAnalysis"]

    def decide_next_tool(self, completed_tools):
        tool_dependencies = {
            "ErrorExtraction": [],
            "SemanticGrouping": ["ErrorExtraction"],
            "FrequencyAnalysis": ["SemanticGrouping"]
        }

        valid_tools = [
            tool for tool, deps in tool_dependencies.items()
            if tool not in completed_tools and all(d in completed_tools for d in deps)
        ]

        if not valid_tools:
            return "DONE"

        prompt = (
            "You are an intelligent log analysis agent.\n"
            f"Completed tools: {list(completed_tools)}\n"
            f"Available tools you MAY choose from: {valid_tools}\n"
            "Choose exactly ONE tool.\n"
            "Reply with ONLY the tool name."
        )

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict tool-selection agent."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    def run_tool(self, tool_name, log_chunks):
        if tool_name == "ErrorExtraction":
            all_errors, timestamps = [], []
            for chunk in log_chunks:
                errors, ts = extract_errors_py(chunk)
                all_errors.extend(errors)
                timestamps.extend(ts)
            self.memory.save("all_errors", all_errors)
            self.memory.save("timestamps", timestamps)
            return f"Extracted {len(all_errors)} errors."

        elif tool_name == "SemanticGrouping":
            errors = self.memory.load("all_errors")
            grouped_errors = group_errors_py(errors)
            self.memory.save("grouped_errors", grouped_errors)
            return f"Grouped {len(grouped_errors)} error clusters."

        elif tool_name == "FrequencyAnalysis":
            errors = self.memory.load("all_errors")
            timestamps = self.memory.load("timestamps")
            freq_stats = analyze_frequency_py(errors, timestamps)
            self.memory.save("frequency_stats", freq_stats)
            return "Frequency analysis completed."

        else:
            return f"Unknown tool: {tool_name}"

    def run(self, log_chunks):
        completed_tools = set()

        while True:
            next_tool = self.decide_next_tool(completed_tools)

            if next_tool == "DONE":
                break

            output = self.run_tool(next_tool, log_chunks)
            completed_tools.add(next_tool)

            print(f"[AGENT] Executed {next_tool}: {output}")

        freq_stats = self.memory.load("frequency_stats")
        grouped_errors = self.memory.load("grouped_errors")

        if freq_stats is None:
            raise RuntimeError(
                "FrequencyAnalysis was not executed. Cannot generate report."
            )

        report_text = generate_summary(grouped_errors, freq_stats, self.client)
        self.memory.save("final_report", report_text)
        save_report_as_pdf(report_text)

        print("[AGENT] Executive summary generated and PDF saved.")
        return report_text
