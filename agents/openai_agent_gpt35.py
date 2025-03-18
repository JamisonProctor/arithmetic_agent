from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from tools.arithmetic_tools import basic_tools
from core.assistant_builder import build_assistant_with_tools

# Load system prompt from Markdown file
with open("prompts/basic_prompt.md", "r") as f:
    prompt = f.read()
sys_msg = SystemMessage(content=prompt)

# Create LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(basic_tools, parallel_tool_calls=True)

# Build agent
agent_graph = build_assistant_with_tools(llm, basic_tools, sys_msg)