import os
import json
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Load evaluation prompt from file
with open("prompts/evaluation_prompt.md", "r") as f:
    EVAL_PROMPT_TEMPLATE = f.read()

# Load final evaluation summary prompt
with open("prompts/evaluation_summary_prompt.md", "r") as f:
    SUMMARY_PROMPT_TEMPLATE = f.read()

def save_combined_evaluations(evaluations, output_dir):
    combined_path = Path(output_dir) / "all_evaluations.json"
    with open(combined_path, "w") as f:
        json.dump(evaluations, f, indent=2)

# --- Parse log file content ---
def parse_log_file(log_path):
    with open(log_path, "r") as f:
        content = f.read()

    try:
        model = content.split("# Model:")[1].split("\n")[0].strip()
        problem_id = content.split("## Word Problem ID:")[1].split("\n")[0].strip()
        system_prompt = content.split("## System Prompt")[1].split("## Word Problem")[0].strip()
        problem_text = content.split("## Word Problem")[1].split("## Agent Messages")[0].strip()
        agent_messages = content.split("## Agent Messages")[1].split("## Ground Truth Solution")[0].strip()
        solution_text = content.split("## Ground Truth Solution")[1].strip()
    except Exception as e:
        raise ValueError(f"Malformed log file {log_path}: {e}")

    return {
        "model": model,
        "problem_id": problem_id,
        "system_prompt": system_prompt,
        "problem_text": problem_text,
        "agent_messages": agent_messages,
        "solution_text": solution_text
    }

# --- Evaluate single file using GPT-4o ---

    

# --- Entry point ---
if __name__ == "__main__":
   # run_all_evaluations()