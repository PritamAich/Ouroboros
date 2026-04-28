from utils.llm import call_llm
from utils.prompts import get_debugger_prompt

def fix_code(code, error):
    prompt = get_debugger_prompt(code, error)

    response = call_llm(prompt)
    return response 