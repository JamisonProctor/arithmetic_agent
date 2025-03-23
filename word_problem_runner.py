import os
from pathlib import Path
from core.agent_loader import load_agent
from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

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
def save_run_log(model_name, problem_id, system_prompt, problem_text, solution_text, agent_output, tool_calls_log, output_dir="logs"):
    os.makedirs(output_dir, exist_ok=True)
    log_path = Path(output_dir) / f"{model_name}__{problem_id}.md"

    with open(log_path, "w") as f:
        f.write(f"# Model: {model_name}\n")
        f.write(f"## Word Problem ID: {problem_id}\n\n")

        f.write("## System Prompt\n")
        f.write(system_prompt.strip() + "\n\n")

        f.write("## Word Problem\n")
        f.write(problem_text.strip() + "\n\n")

        f.write("## Agent Messages\n")

        tool_call_iter = iter(tool_calls_log)
        tool_call_index = 0


        for i, msg in enumerate(agent_output["messages"]):
            role = msg.type.upper()
            if "[TOOL CALL]" in msg.content:
                f.write(f"### Step {i+1} (TOOL CALL)\n")
            else:
                f.write(f"### Step {i+1} ({role})\n")
            f.write(msg.content.strip() + "\n\n")

        f.write("## Ground Truth Solution\n")
        f.write(solution_text.strip() + "\n")

# --- Run all problems for a specific model ---
def run_all_problems_for_model(model_name, problem_dir="word_problems"):
    # Prepare tool_calls_log for logging tool calls
    tool_calls_log = []

    # Load agent graph (now also returns log reference)
    agent_graph, tool_calls_log = load_agent(model_name)

    # Load system prompt to include in logs
    with open("prompts/basic_prompt.md", "r") as f:
        system_prompt = f.read()

    # Iterate over all markdown problem files
    problem_files = sorted(Path(problem_dir).glob("problem_*.md"))
    for problem_path in problem_files:
        problem_id = problem_path.stem.replace("problem_", "")
        print(f"Running {model_name} on problem {problem_id}...")

        # Clear the log for each problem
        tool_calls_log.clear()

        # Load problem text and ground truth solution
        problem_text, solution_text = load_problem_content(problem_path)

        # Prepare messages and invoke agent
        messages = [HumanMessage(content=problem_text)]
        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 100}
        result = agent_graph.invoke({"messages": messages}, config=config)

        # Save full output trace, now including tool call log
        save_run_log(model_name, problem_id, system_prompt, problem_text, solution_text, result, tool_calls_log)

    print(f"✅ Completed all problems for model: {model_name}")

# --- Entry point ---
if __name__ == "__main__":
    for model in [
        "gpt-3.5-turbo", 
        "gpt-4o", 
        #"llama3.1", 
        #"granite3.2", 
        #"mistral-nemo", 
        #"qwen2.5"
        ]: 
        run_all_problems_for_model(model)