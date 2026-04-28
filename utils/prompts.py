def get_coder_prompt(user_task):
    return f"""
You are a Python expert.

Write a Python program for the following task:
{user_task}

Rules:
- Use a function for logic
- Do NOT rely on command line arguments (no sys.argv)
- Do NOT use input()
- Include a sample execution inside the script
- Ensure the program prints output when run
- All import statements must be at the top of the file, never inside functions
- If the task requires reading an external file, use a clearly named 
  placeholder filename like 'sample.csv'. Do NOT call the function 
  anywhere in the script. Do NOT include any sample execution. 
  Only add a comment at the bottom showing how to call it.
  The function itself should be complete and correct.
- Return ONLY executable Python code. No explanations. No markdown.
"""

def get_debugger_prompt(code, error):
    return f"""
You are a strict Python debugger.

The following Python code produced an error when executed.

CODE:
{code}

ERROR:
{error}

Your job:
- Fix the code so it runs without errors
- Do NOT change what the code is supposed to do
- Do NOT include explanations
- Do NOT include markdown
- Return ONLY clean executable Python code
"""

def get_tester_prompt(code, user_task):
    return f"""
You are a strict Python code reviewer.

The following code was written to complete this task:
TASK: {user_task}

CODE:
{code}

Carefully read the code and answer:
1. Does this code correctly complete the task?
2. Is the core logic correct? For example, if the task asks for highest values, 
   verify the sorting direction is correct. If the task asks for a sum, verify 
   the operation is addition not subtraction.
3. If not, what is the CRITICAL logical problem?

Important rules:
- Only fail the code if there is a CRITICAL logical problem
- Do NOT fail code over minor style issues or unnecessary imports
- Do NOT fail code over hypothetical edge cases not mentioned in the task
- DO fail code if the logic produces obviously wrong results

Reply in this exact format:
PASS: <yes or no>
REASON: <one sentence explanation>
"""