# Model: llama3.1
## Word Problem ID: 005

## System Prompt
# Math Agent Prompt (System Message)

You are a math-solving agent. You MUST use a tool for every arithmetic operation — you are not allowed to solve anything in your head.

## Behavioral Rules
1. Think through the problem step by step and write out your thoughts.
2. Describe your reasoning clearly in writing BEFORE calling any tool.
3. Call ONLY ONE tool per step. Never call more than one tool in a single message.
4. WAIT for the result before deciding what to do next.
5. Do not give a final answer until all tool results are available and reasoning is complete.
6. If you want to calculate anything, you MUST call a tool. You cannot do math on your own.

## Tools Available
- `add(a, b)` — Add two numbers.
- `subtract(a, b)` — Subtract second number from first.
- `multiply(a, b)` — Multiply two numbers.
- `divide(a, b)` — Divide first number by second.

## Reminder
CALL ONLY ONE TOOL AT A TIME. NEVER call multiple tools in a single message.

## Word Problem
A student chose a number, multiplied it by 2, then subtracted 138 from the result and got 102.  
What was the number he chose?

## Agent Messages
### Step 1 (HUMAN)
A student chose a number, multiplied it by 2, then subtracted 138 from the result and got 102.  
What was the number he chose?

### Step 2 (AI)


### Step 3 (TOOL CALL)
[TOOL CALL] add(a=138, b=102) -> 240

### Step 4 (TOOL)
240

### Step 5 (AI)


### Step 6 (TOOL CALL)
[TOOL CALL] divide(a=240, b=2) -> 120.0

### Step 7 (TOOL)
120.0

### Step 8 (AI)
The student chose the number 120.

## Ground Truth Solution
The number he chose was 120.
