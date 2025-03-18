from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from tools.arithmetic_tools import basic_tools
from core.assistant_builder import build_assistant_with_tools

# Load system prompt from Markdown file
with open("prompts/basic_prompt.md", "r") as f:
    prompt = f.read()
sys_msg = SystemMessage(content=prompt)

# Create LLM (note: no parallel_tool_calls support in Ollama)
llm = ChatOllama(model="llama3.1", temperature=0)
llm_with_tools = llm.bind_tools(basic_tools)  # no parallel_tool_calls param

# Build agent
agent_graph = build_assistant_with_tools(llm, basic_tools, sys_msg)