from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from tools.arithmetic_tools import basic_tools
from core.assistant_builder import build_assistant_with_tools

def load_agent(model_name: str):
    # Load the system prompt
    with open("prompts/basic_prompt.md", "r") as f:
        prompt = f.read()
    sys_msg = SystemMessage(content=prompt)

    # OpenAI models (GPT 3.5 / 4o)
    if model_name == "gpt-3.5-turbo":
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        llm_with_tools = llm.bind_tools(basic_tools, parallel_tool_calls=True)

    elif model_name == "gpt-4o":
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        llm_with_tools = llm.bind_tools(basic_tools, parallel_tool_calls=True)

    # Ollama / LLaMA models
    elif model_name == "llama3-8b":
        llm = ChatOllama(model="llama3.1:8b", temperature=0)
        llm_with_tools = llm.bind_tools(basic_tools)

    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # Return compiled agent graph
    return build_assistant_with_tools(llm, basic_tools, sys_msg)