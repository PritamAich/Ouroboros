from utils.llm import call_llm
from utils.prompts import get_coder_prompt

def generate_code(user_task):
    prompt =  get_coder_prompt(user_task)

    response = call_llm(prompt)

    return response