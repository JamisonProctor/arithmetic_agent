# core/tool_call_logger.py

from langchain_core.messages import ToolMessage
from langgraph.graph import MessagesState

class ToolCallLogger:
    def __init__(self, tools, log_list):
        self.tools = tools
        self.log_list = log_list

    def __call__(self, state: MessagesState):
        last_message = state["messages"][-1]
        tool_messages = []

        if hasattr(last_message, "tool_calls"):
            tool_calls = last_message.tool_calls

            for call in tool_calls:
                name = call.get("name")
                args = call.get("args", {})
                tool_call_id = call.get("id")

                # Log tool call string
                args_str = ", ".join(f"{k}={v}" for k, v in args.items())
                tool_call_str = f"{name}({args_str})"
                self.log_list.append(tool_call_str)

                # Match tool by function name (not .name — your tools are regular functions)
                tool_func = next((t for t in self.tools if t.__name__ == name), None)

                if not tool_func:
                    result = f"[ERROR: Unknown tool '{name}']"
                else:
                    try:
                        result = tool_func(**args)
                    except Exception as e:
                        result = f"[ERROR: {str(e)}]"

                tool_messages.append(ToolMessage(tool_call_id=tool_call_id, content=str(result)))

        return {"messages": tool_messages}