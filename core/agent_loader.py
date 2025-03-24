from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from tools import arithmetic_tools
from core.assistant_builder import build_assistant_with_tools, build_assistant_with_tools_and_logging
from dotenv import load_dotenv
import os

load_dotenv()

def load_agent(model_name: str):
    # Load the system prompt
    with open("prompts/basic_prompt.md", "r") as f:
        prompt = f.read()
    sys_msg = SystemMessage(content=prompt)

    tool_calls_log = []
    tools = [t["func"] for t in arithmetic_tools.basic_tools]  # Extract only the function list

    # Initialize model
    if model_name == "gpt-3.5-turbo":
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    elif model_name == "gpt-4o":
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
    elif model_name == "llama3.1":
        llm = ChatOllama(model="llama3.1", temperature=0)
    elif model_name == "granite3.2":
        llm = ChatOllama(model="granite3.2", temperature=0)
    elif model_name == "mistral-nemo":
        llm = ChatOllama(model="mistral-nemo", temperature=0)
    elif model_name == "qwen2.5":
        llm = ChatOllama(model="qwen2.5", temperature=0)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # ✅ ALWAYS bind tools regardless of model
    llm_with_tools = llm.bind_tools(tools)

    if model_name in {"gpt-3.5-turbo", "gpt-4o"}:
        agent_graph = build_assistant_with_tools(llm_with_tools, tools, sys_msg)
        return agent_graph, []
    else:
        agent_graph = build_assistant_with_tools_and_logging(llm_with_tools, tools, sys_msg, tool_calls_log)
        return agent_graph, tool_calls_log