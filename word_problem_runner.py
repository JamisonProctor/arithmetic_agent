import os
from pathlib import Path
from core.agent_loader import load_agent
from langchain_core.messages import HumanMessage

# --- Load problem and solution from markdown ---
def load_problem_content(problem_path):
    with open(problem_path, "r") as f:
        content = f.read()
    try:
        problem = content.split("## Solution")[0].split("## Problem")[1].strip()
        solution = content.split("## Solution")[1].strip()
    except IndexError:
        raise ValueError(f"Malformed markdown in {problem_path}")
    return problem, solution

# --- Save full trace log as markdown ---
def save_run_log(model_name, problem_id, system_prompt, problem_text, solution_text, agent_output, output_dir="logs"):
    os.makedirs(output_dir, exist_ok=True)
    log_path = Path(output_dir) / f"{model_name}__{problem_id}.md"
    with open(log_path, "w") as f:
        f.write(f"# Model: {model_name}\n")
        f.write(f"## Word Problem ID: {problem_id}\n\n")
        
        f.write("## System Prompt\n")
        f.write(system_prompt.strip() + "\n\n")

        f.write("## Word Problem\n")
        f.write(problem_text.strip() + "\n\n")

        f.write("## Ground Truth Solution\n")
        f.write(solution_text.strip() + "\n\n")

        f.write("## Agent Messages\n")
        for i, msg in enumerate(agent_output["messages"]):
            role = msg.type.upper()
            f.write(f"### Step {i+1} ({role})\n")
            f.write(str(msg.content).strip() + "\n\n")

# --- Run all problems for a specific model ---
def run_all_problems_for_model(model_name, problem_dir="word_problems"):
    agent_graph = load_agent(model_name)

    # Load system prompt to include in logs
    with open("prompts/basic_prompt.md", "r") as f:
        system_prompt = f.read()

    # Iterate over all markdown problem files
    problem_files = sorted(Path(problem_dir).glob("problem_*.md"))
    for problem_path in problem_files:
        problem_id = problem_path.stem.replace("problem_", "")
        print(f"Running {model_name} on problem {problem_id}...")

        # Load problem text and ground truth solution
        problem_text, solution_text = load_problem_content(problem_path)

        # Prepare messages and invoke agent
        messages = [HumanMessage(content=problem_text)]
        result = agent_graph.invoke({"messages": messages})

        # Save full output trace
        save_run_log(model_name, problem_id, system_prompt, problem_text, solution_text, result)

    print(f"✅ Completed all problems for model: {model_name}")

# --- Entry point ---
if __name__ == "__main__":
    for model in ["gpt-3.5-turbo", "gpt-4o", "llama3-8b"]:
        run_all_problems_for_model(model)