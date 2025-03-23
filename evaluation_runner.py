import os
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from evaluation.evaluation_questions import evaluation_questions
from evaluation.evaluation_utils import parse_log_file, evaluate_question

# Setup LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Directories
LOGS_DIR = "logs"
OUTPUT_DIR = "evaluations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all log files
log_files = sorted(Path(LOGS_DIR).glob("*.md"))

for log_file in log_files:
    model_name = log_file.name.split("__")[0]
    problem_id = log_file.name.split("__")[1].split(".")[0]
    output_path = Path(OUTPUT_DIR) / f"{model_name}__{problem_id}.json"

    print(f"Evaluating {model_name} on problem {problem_id}...")

    # Load sections
    log_sections = parse_log_file(log_file)

    # Run evaluation one question at a time
    eval_results = {}
    for i, question in enumerate(evaluation_questions):
        print(f"  Q{i+1}: {question}")
        try:
            eval_response = evaluate_question(llm, log_sections, question)
        except Exception as e:
            eval_response = {
                "answer": "error",
                "comment": f"Error during evaluation: {str(e)}"
            }

        eval_results[f"Q{i+1}"] = {
            "question": question,
            "answer": eval_response.get("answer", "error"),
            "comment": eval_response.get("comment", "")
        }

        # Save intermediate results in case of interruption
        with open(output_path, "w") as f:
            json.dump(eval_results, f, indent=2)

print("✅ Evaluation complete for all log files.")