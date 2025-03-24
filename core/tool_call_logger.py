from langchain_core.messages import ToolMessage, AIMessage

class ToolCallLogger:
    def __init__(self, tools, tool_calls_log):
        self.tool_map = {t["name"]: t["func"] for t in tools}
        self.tool_calls_log = tool_calls_log

    def __call__(self, state):
        last_msg = state["messages"][-1]
        tool_calls = getattr(last_msg, "tool_calls", [])

        new_messages = []

        for call in tool_calls:
            name = call.get("name")
            args = call.get("args", {})
            tool_call_id = call.get("id", None)
            if not tool_call_id:
                tool_call_id = f"fallback-{name}"

            # Format args as string for logging
            arg_str = ', '.join(f"{k}={v}" for k, v in args.items())
            call_str = f"{name}({arg_str})"

            try:
                tool_func = self.tool_map.get(name)
                result = tool_func(**args)
                result_str = str(result)
                log_entry = f"[TOOL CALL] {call_str} -> {result_str}"
            except Exception as e:
                result_str = f"[TOOL ERROR] {str(e)}"
                log_entry = f"[TOOL CALL] {call_str} -> ERROR: {str(e)}"

            # Log for external use (file logs, eval, etc.)
            self.tool_calls_log.append(log_entry)

            # 🔥 Inject visible inline message BEFORE the ToolMessage
            new_messages.append(AIMessage(content=f"[TOOL CALL] {call_str}"))

            # Then emit the actual ToolMessage result (still needed for tool chaining)
            new_messages.append(ToolMessage(tool_call_id=tool_call_id, content=result_str))

        return {"messages": new_messages}