# core/assistant_builder.py

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition
from core.tool_call_logger import ToolCallLogger

def build_assistant_with_tools(llm, tools, sys_msg):
    def assistant(state):
        return {"messages": [llm.bind_tools(tools).invoke([sys_msg] + state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    return builder.compile()

def build_assistant_with_tools_and_logging(llm, tools, sys_msg, tool_log_list):
    def assistant(state):
        return {"messages": [llm.bind_tools(tools).invoke([sys_msg] + state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolCallLogger(tools, tool_log_list))  # Logging-enhanced tool node
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)  # ✅ Fixed line here
    builder.add_edge("tools", "assistant")

    return builder.compile()