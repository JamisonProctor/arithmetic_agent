evaluation_questions = [
    "In the first AI response, does the model explain its approach or reasoning before any tool call is made?",
    "Does the model initiate tool calls during the interaction (evidenced by TOOL steps following AI steps)?",
    "When the model makes tool calls, are they formatted correctly using tool name and arguments (e.g., add(a, b))?",
    "If the model makes incorrect or incomplete tool calls, does it correct the mistake and successfully call the tool in a later step?",
    "Does the model rely solely on tool calls for all arithmetic steps, or does it skip tools and do calculations directly in AI responses?",
    "Does the model provide a complete step-by-step solution, leading to a final answer for the problem?",
    "Is the final answer provided by the model the same as the ground truth solution shown at the end of the log?"
]