# Model: qwen2.5
## Word Problem ID: 001

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
A salesman sold twice as much pears in the afternoon than in the morning.  
If he sold 360 kilograms of pears that day, how many kilograms did he sell in the morning and how many in the afternoon?

## Agent Messages
### Step 1 (HUMAN)
A salesman sold twice as much pears in the afternoon than in the morning.  
If he sold 360 kilograms of pears that day, how many kilograms did he sell in the morning and how many in the afternoon?

### Step 2 (AI)


### Step 3 (TOOL)
120.0

### Step 4 (AI)


### Step 5 (TOOL)
240

### Step 6 (AI)
The salesman sold 120 kilograms of pears in the morning. In the afternoon, he sold twice as much, which is 240 kilograms.

So, he sold 120 kilograms in the morning and 240 kilograms in the afternoon.

## Ground Truth Solution

- Morning: 120 kg
- Afternoon: 240 kg
