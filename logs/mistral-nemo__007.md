# Model: mistral-nemo
## Word Problem ID: 007

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
One side of a rectangle is 3 cm shorter than the other side.  
If we increase the length of each side by 1 cm, then the area of the rectangle will increase by 18 cm².  
Find the lengths of all sides.

## Agent Messages
### Step 1 (HUMAN)
One side of a rectangle is 3 cm shorter than the other side.  
If we increase the length of each side by 1 cm, then the area of the rectangle will increase by 18 cm².  
Find the lengths of all sides.

### Step 2 (AI)
Let's denote the length of the shorter side as x. Then the longer side is x + 3.

The original area of the rectangle is x(x + 3).

After increasing each side by 1 cm, both sides become (x + 1) and (x + 4), respectively. So the new area is (x + 1)(x + 4).

According to the problem, the increase in area is 18 cm²:

(x + 1)(x + 4) - x(x + 3) = 18

Expanding both sides:

x^2 + 5x + 4 - x^2 - 3x = 18

Simplifying:

2x + 4 = 18

Subtracting 4 from both sides:

2x = 14

Dividing by 2:

x = 7

So the shorter side is 7 cm and the longer side is 7 + 3 = 10 cm.

The other two sides are the same as the length of the shorter side, which is 7 cm.

## Ground Truth Solution
The sides of the rectangle are 10 cm and 7 cm.
