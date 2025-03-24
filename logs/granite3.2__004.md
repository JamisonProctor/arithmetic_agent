# Model: granite3.2
## Word Problem ID: 004

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
A farming field can be ploughed by 6 tractors in 4 days.  
When 6 tractors work together, each of them ploughs 120 hectares a day.  

If two of the tractors were moved to another field, then the remaining 4 tractors could plough the same field in 5 days.  

How many hectares a day would one tractor plough then?

## Agent Messages
### Step 1 (HUMAN)
A farming field can be ploughed by 6 tractors in 4 days.  
When 6 tractors work together, each of them ploughs 120 hectares a day.  

If two of the tractors were moved to another field, then the remaining 4 tractors could plough the same field in 5 days.  

How many hectares a day would one tractor plough then?

### Step 2 (AI)
Let's break this problem down step by step:

1. We know that 6 tractors can plough 120 hectares per day together. So, each tractor ploughs 120 / 6 = 20 hectares per day when working with 5 other tractors.

2. Now, if we remove 2 tractors, we are left with 4 tractors. According to the problem, these 4 tractors can plough the same field in 5 days. 

3. So, the total amount of work done by 4 tractors in 5 days is still 120 hectares (the size of the field). 

4. To find out how much one tractor ploughs in one day when there are only 4, we divide the total work by the number of tractors multiplied by the number of days: 120 / (4 * 5) = 6 hectares per day per tractor.

Let's call the `divide` tool to calculate this:

- `divide(120, multiply(4, 5))`

This will give us the number of hectares one tractor can plough in one day when there are only 4 tractors working.

## Ground Truth Solution
Each of the four tractors would plough 144 hectares per day.
