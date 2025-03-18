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
def evaluate_with_llm(log_data, eval_model):
    prompt = EVAL_PROMPT_TEMPLATE + f"""

## System Prompt:
{log_data['system_prompt']}

## Word Problem:
{log_data['problem_text']}

## Agent Message Trace:
{log_data['agent_messages']}

## Ground Truth Solution:
{log_data['solution_text']}
"""
    messages = [SystemMessage(content="You are a rigorous evaluator."), HumanMessage(content=prompt)]
    result = eval_model.invoke(messages)
    return result.content.strip()

# --- Main runner ---
def run_all_evaluations(log_dir="logs", output_dir="evaluations"):
    os.makedirs(output_dir, exist_ok=True)
    eval_model = ChatOpenAI(model="gpt-4o", temperature=0)

    evaluations = []
    per_model_scores = defaultdict(list)

    log_files = sorted(Path(log_dir).glob("*.md"))
    for log_path in log_files:
        print(f"Evaluating: {log_path.name}")
        log_data = parse_log_file(log_path)

        try:
            raw_eval = evaluate_with_llm(log_data, eval_model)
            eval_json = json.loads(raw_eval)

        except Exception as e:
            print(f"⚠️ Failed to parse evaluation for {log_path.name}: {e}")
            eval_json = {
                "model": log_data['model'],
                "problem_id": log_data['problem_id'],
                "error": str(e),
                "raw_output": raw_eval
            }

        evaluations.append(eval_json)
        if "reasoning_score" in eval_json:
            per_model_scores[eval_json["model"]].append(eval_json["reasoning_score"])

        # Save individual evaluation JSON
        eval_path = Path(output_dir) / f"{log_data['model']}__{log_data['problem_id']}.json"
        with open(eval_path, "w") as f:
            json.dump(eval_json, f, indent=2)

    # Save combined evaluation report
    combined_path = Path(output_dir) / "all_evaluations.json"
    with open(combined_path, "w") as f:
        json.dump(evaluations, f, indent=2)

    # Print model-level summary
    print("\n📊 Evaluation Summary (Reasoning Score Averages):")
    for model, scores in per_model_scores.items():
        avg = round(sum(scores) / len(scores), 2)
        print(f"{model}: {avg}")

# --- Entry point ---
if __name__ == "__main__":
    run_all_evaluations()