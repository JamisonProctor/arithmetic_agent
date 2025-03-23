import os
import json
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Load and parse log file into sections
def parse_log_file(log_path):
    with open(log_path, "r") as f:
        content = f.read()

    def extract_section(title, next_titles):
        try:
            start = content.index(f"## {title}") + len(f"## {title}")
            end = len(content)
            for next_title in next_titles:
                if f"## {next_title}" in content[start:]:
                    end = start + content[start:].index(f"## {next_title}")
                    break
            return content[start:end].strip()
        except ValueError:
            return ""

    return {
        "system_prompt": extract_section("System Prompt", ["Word Problem", "Agent Messages", "Ground Truth Solution"]),
        "problem": extract_section("Word Problem", ["Agent Messages", "Ground Truth Solution"]),
        "agent_messages": extract_section("Agent Messages", ["Ground Truth Solution"]),
        "ground_truth": extract_section("Ground Truth Solution", [])
    }

# Format the prompt for a single evaluation question
def build_eval_prompt(log_sections, question_text):
    return f"""You are an evaluator judging the behavior of an AI assistant solving a math problem using tool calls.

Carefully read the full agent interaction below, along with the system prompt and the correct ground truth solution.

Then answer the evaluation question shown at the end.

### BEGIN EVALUATION INPUT

--- SYSTEM PROMPT ---
{log_sections["system_prompt"]}

--- WORD PROBLEM ---
{log_sections["problem"]}

--- AGENT INTERACTION ---
{log_sections["agent_messages"]}

--- GROUND TRUTH SOLUTION ---
{log_sections["ground_truth"]}

Agent Messages are formatted in distinct steps, each prefixed by a role label: HUMAN, AI, or TOOL.

Steps labeled (AI) are messages authored by the agent itself.
Steps labeled (TOOL) are tool outputs the agent receives in response to tool calls.

When evaluating whether the agent described its approach before calling tools, consider whether there is a thoughtful AI message before any TOOL step appears.

--- EVALUATION QUESTION ---
{question_text}

Answer using a short one-word response ("yes", "no", or "other") followed by one or two sentences of explanation.
"""

# Call GPT-4o to evaluate a single question
def evaluate_question(llm, log_sections, question_text):
    prompt = build_eval_prompt(log_sections, question_text)
    msg = [HumanMessage(content=prompt)]
    response = llm.invoke(msg)
    response_text = response.content.strip()

    if not response_text:
        return {
            "answer": "error",
            "comment": "Model returned an empty response."
        }

    # Extract answer from first non-empty line
    lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    first_line = lines[0].lower() if lines else ""
    first_word = first_line.split()[0].strip(" .:") if first_line else "other"

    if first_word not in ["yes", "no", "other"]:
        first_word = "other"

    comment = response_text.strip()
    return {"answer": first_word, "comment": comment}