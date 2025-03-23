# Model: mistral-nemo
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
[TOOL_CALLS] Let's denote the number of kilograms of pears sold in the morning as x. According to the problem, twice that amount was sold in the afternoon, so we can express the afternoon sales as 2x.

The total sales for the day were 360 kilograms, which is the sum of the morning and afternoon sales. Therefore, we can write the equation:

x + 2x = 360

Combining like terms, we get:

3x = 360

To find the value of x, we need to divide both sides of the equation by 3:

```json
{
  "function": "divide",
  "arguments": {
    "a": 360,
    "b": 3
  }
}
```

Let's wait for the result before proceeding.

## Ground Truth Solution
- Morning: 120 kg
- Afternoon: 240 kg
