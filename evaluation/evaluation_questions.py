evaluation_questions = [
    "Does the model describe its approach to the solution before calling any tools?",
    "Does the model attempt to call any tools?",
    "Does the model use correct syntax/format for the tool calls?",
    "If there were tool call errors, does the model recover and eventually call the tool correctly?",
    "Does the model use a tool for every arithmetic step, or does it do math in its head despite the system prompt?",
    "Does the model attempt a complete solution to the problem?",
    "Is the final answer correct compared to the ground truth solution?"
]