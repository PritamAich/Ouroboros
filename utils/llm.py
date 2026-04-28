import requests
import re

def extract_code(text):
    # Extract code inside ``` blocks
    code_blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)

    if code_blocks:
        return code_blocks[0].strip()

    return text.strip()  # fallback if no code block

def call_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:3b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        # ✅ Safe extraction
        if "response" in data:
            return extract_code(data["response"])
        else:
            print("Unexpected response:", data)
            return ""

    except Exception as e:
        print("LLM Error:", str(e))
        return ""