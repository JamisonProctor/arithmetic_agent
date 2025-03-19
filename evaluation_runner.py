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
    
    messages = [
        SystemMessage(content="You are a strict JSON-only evaluation agent. Respond ONLY with valid JSON. Do not include any markdown or explanation."),
        HumanMessage(content=prompt)
    ]
    
    result = eval_model.invoke(messages)
    raw_output = result.content.strip()

    # Clean up GPT-4o Markdown wrapping if present
    if raw_output.startswith("```json"):
        raw_output = raw_output.strip("```json").strip("```").strip()
    elif raw_output.startswith("```"):
        raw_output = raw_output.strip("```").strip()

    return raw_output

def generate_model_summary_evaluation(model_name, model_evals, eval_model, output_dir, log_dir="logs"):
    model_problem_ids = [e["problem_id"] for e in model_evals if e.get("problem_id") != "overall"]
    combined_blocks = []

    for pid in model_problem_ids:
        log_path = Path(log_dir) / f"{model_name}__{pid}.md"
        eval_data = next((e for e in model_evals if e["problem_id"] == pid), None)

        if not eval_data or not log_path.exists():
            continue

        with open(log_path, "r") as f:
            log_content = f.read()

        block = f"""---\n## Problem ID: {pid}\n\n### Log Content:\n{log_content}\n\n### Evaluation Summary:\n{json.dumps(eval_data, indent=2)}"""
        combined_blocks.append(block)

    full_context = "\n\n".join(combined_blocks)

    # Calculate % correct answers
    total = len(model_evals)
    correct = sum(1 for e in model_evals if e.get("correct_final_answer") is True)
    correct_final_answer_percent = round((correct / total) * 100, 1) if total > 0 else 0.0

    summary_prompt = SUMMARY_PROMPT_TEMPLATE + f"""

        This model solved {correct} out of {total} problems correctly, for a final answer accuracy of {correct_final_answer_percent}%.
        Use this information as part of your overall evaluation.

        Here is the full context of logs and JSON evaluations:
        {full_context}
    """

    messages = [
        SystemMessage(content="You are a strict JSON-only evaluator. Respond ONLY in the format provided."),
        HumanMessage(content=summary_prompt.strip())
    ]

    result = eval_model.invoke(messages)
    summary_output = result.content.strip()

    # Clean up triple-backtick formatting
    if summary_output.startswith("```json"):
        summary_output = summary_output.strip("```json").strip("```").strip()
    elif summary_output.startswith("```"):
        summary_output = summary_output.strip("```").strip()

    try:
        summary_json = json.loads(summary_output)
    except Exception as e:
        summary_json = {
            "model": model_name,
            "problem_id": "overall",
            "error": f"Failed to parse model summary: {e}",
            "raw_output": summary_output
        }

    # Add manually computed accuracy to JSON regardless of GPT output
    summary_json["correct_final_answer_percent"] = correct_final_answer_percent

    out_path = Path(output_dir) / f"{model_name}__overall.json"
    with open(out_path, "w") as f:
        json.dump(summary_json, f, indent=2)

    return summary_json

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
    save_combined_evaluations(evaluations, output_dir)

    # Print model-level summary
    print("\n📊 Evaluation Summary (Reasoning Score Averages):")
    for model, scores in per_model_scores.items():
        avg = round(sum(scores) / len(scores), 2)
        print(f"{model}: {avg}")

    # Final model summary evaluations
    print("\n🧠 Generating overall summary evaluation per model...")
    for model in per_model_scores:
        model_evals = [e for e in evaluations if e.get("model") == model and e.get("problem_id") != "overall"]
        summary = generate_model_summary_evaluation(model, model_evals, eval_model, output_dir)
        evaluations.append(summary)

    # Save combined evaluations again (with summary included)
    save_combined_evaluations(evaluations, output_dir)
    

# --- Entry point ---
if __name__ == "__main__":
    run_all_evaluations()