from agents.coder import generate_code
from agents.tester import test_code
from agents.debugger import fix_code
from utils.executor import run_code
import re
import os

def save_code(code, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(code)

def clean_code(code):
    # Remove markdown code fences if LLM includes them
    code = re.sub(r"```(?:python)?(.*?)```", r"\1", code, flags=re.DOTALL)
    
    # Remove known invalid tokens small LLMs sometimes produce
    invalid_patterns = ["end_program", "<|endoftext|>", "<|im_end|>"]
    for pattern in invalid_patterns:
        code = code.replace(pattern, "")
    
    return code.strip()

# ---------- Setup ----------
FILE_PATH = "workspace/generated_code.py"
MAX_ATTEMPTS = 3

user_task = input("Enter your task: ").strip()

if not user_task:
    print("❌ No task entered. Exiting.")
    exit(1)

# ---------- Step 1: Generate ----------
print("\n⚙️  Generating code...\n")
code = generate_code(user_task)

if not code.strip():
    print("❌ Failed to generate code. Try again.")
    exit(1)

# ---------- Step 2: Loop ----------

success = False

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n{'='*40}")
    print(f"🔁 Attempt {attempt} of {MAX_ATTEMPTS}")
    print(f"{'='*40}")

    code = clean_code(code)
    save_code(code, FILE_PATH)

    # Step 2a: Run the code
    output, error = run_code(FILE_PATH)

    if error:
        # Crashed — send straight to debugger
        print("\n❌ Execution error:\n", error)
        print("\n🛠️  Fixing code...\n")
        code = fix_code(code, error)

    else:
        # Ran successfully — now test if it's logically correct
        print("\n✅ Code ran successfully. Testing logic...\n")
        test_result = test_code(code, user_task)

        if test_result["passed"]:
            print("✅ Logic check passed!")
            print("📝 Generated Code:\n")
            print(code)
            print("\n📤 Output:\n", output)
            success = True
            break
        else:
            # Logic is wrong — fix with the tester's reason as the error
            print("⚠️  Logic check failed.")
            print("📝 Reason:", test_result["reason"])
            print("\n🛠️  Fixing code...\n")
            code = fix_code(code, test_result["reason"])

if not success:
    print(f"\n💀 Failed after {MAX_ATTEMPTS} attempts.")
    print("💡 Try simplifying your task description.")