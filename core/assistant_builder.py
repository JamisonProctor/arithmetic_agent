from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
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

def build_assistant_with_tools_and_logging(llm_with_tools, tools, sys_msg, tool_log_list):
    if isinstance(tools, list) and all(callable(t) for t in tools):
        tools = [{"name": t.__name__, "func": t} for t in tools]

    def assistant(state):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolCallLogger(tools, tool_log_list))  # Logging-enhanced tool node
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)  # ✅ Fixed line here
    builder.add_edge("tools", "assistant")

    return builder.compile()