from utils.llm import call_llm
from utils.prompts import get_tester_prompt

def test_code(code, user_task):
    prompt = get_tester_prompt(code, user_task)
    response = call_llm(prompt)
    return parse_test_result(response)

def parse_test_result(response):
    lines = response.strip().splitlines()
    
    result = {
        "passed": False,
        "reason": "No reason provided"
    }

    for line in lines:
        if line.startswith("PASS:"):
            answer = line.replace("PASS:", "").strip().lower()
            result["passed"] = answer == "yes"
        elif line.startswith("REASON:"):
            result["reason"] = line.replace("REASON:", "").strip()

    # Fallback: if LLM ignored the format, assume pass if response 
    # contains positive language
    if result["reason"] == "No reason provided":
        lowered = response.lower()
        if any(word in lowered for word in ["correct", "valid", "pass", "looks good", "works"]):
            result["passed"] = True
            result["reason"] = "Tester response was unstructured but positive"
        else:
            result["passed"] = False
            result["reason"] = "Tester response was unstructured and unclear"

    return result