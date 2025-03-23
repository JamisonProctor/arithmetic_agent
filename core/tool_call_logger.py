from langchain_core.messages import ToolMessage, AIMessage

class ToolCallLogger:
    def __init__(self, tools, tool_log_list):
        self.tools = tools
        self.tool_log_list = tool_log_list
        self.tool_map = {t["name"]: t["func"] for t in tools}

    def __call__(self, state):
        last_msg = state["messages"][-1]
        new_messages = []

        if not hasattr(last_msg, "tool_calls") or not last_msg.tool_calls:
            return state

        for call in last_msg.tool_calls:
            name = call.get("name")
            args = call.get("args", {})
            tool_log_text = f"[TOOL CALL] {name}({', '.join(f'{k}={v}' for k, v in args.items())})"

            try:
                tool_func = self.tool_map.get(name)
                if not tool_func:
                    raise Exception("Unknown tool")

                result = tool_func(**args)
                tool_log_text += f" -> {result}"
                tool_output = ToolMessage(content=str(result), tool_call_id=call.get("id", "unknown"))
            except Exception as e:
                tool_log_text += f" -> ERROR: {e}"
                tool_output = ToolMessage(content=f"[TOOL ERROR] {e}", tool_call_id=call.get("id", "unknown"))

            self.tool_log_list.append(tool_log_text)

            new_messages.append(AIMessage(content=tool_log_text))
            new_messages.append(tool_output)

        return {"messages": state["messages"] + new_messages}