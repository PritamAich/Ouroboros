# 🐍 Ouroboros
### A Self-Healing Multi-Agent Code Generation System

> *Ouroboros — the ancient symbol of a snake consuming its own tail — represents endless self-correction. Just like this system: generate, fail, learn, fix, repeat.*

---

## 🧠 What Is This?

Ouroboros is a multi-agent AI system that takes a plain English task from the user, writes Python code to solve it, tests whether the code is logically correct, and automatically debugs and fixes it — all without human intervention.

It was built as a hands-on learning project to explore two key areas of modern AI engineering:

- **Prompt Engineering** — how the wording of instructions to an LLM directly determines the quality of its output
- **Multi-Agent Systems** — how multiple specialized AI agents can collaborate in a pipeline to produce results no single agent could achieve alone

---

## 🔄 How It Works

```
User Task (plain English)
        ↓
  [ Coder Agent ]        →  Generates Python code
        ↓
  [ Executor ]           →  Runs the code in a sandbox
        ↓
  ┌─────┴─────┐
crash?       no crash?
  ↓               ↓
[ Debugger ]   [ Tester Agent ]   →  Checks logical correctness
  ↑               ↓         ↓
  └─────────── failed?    passed?
                  ↓               ↓
            [ Debugger ]      Print Output ✅
```

The system retries up to **3 times** before gracefully giving up with a helpful message.

---

## 🤖 The Agents

| Agent | File | Role |
|---|---|---|
| **Coder** | `agents/coder.py` | Generates Python code from a plain English task |
| **Tester** | `agents/tester.py` | Reviews code logic and checks if it actually solves the task |
| **Debugger** | `agents/debugger.py` | Fixes code based on execution errors or tester feedback |

---

## 🗂️ Project Structure

```
Ouroboros/
│
├── main.py                  # Entry point — orchestrates the full pipeline
├── agents/
│   ├── coder.py             # Code generation agent
│   ├── tester.py            # Logic testing agent
│   └── debugger.py          # Code fixing agent
│
├── utils/
│   ├── llm.py               # LLM API calls and response parsing
│   ├── executor.py          # Sandboxed code execution
│   └── prompts.py           # All prompt templates in one place
│
└── workspace/
    └── generated_code.py    # Where generated code lives during execution
```

---

## 💡 Key Design Decisions

### 1. Centralized Prompts (`utils/prompts.py`)
All LLM prompts live in a single file. This was a deliberate choice — when doing prompt engineering, you should never be hunting through multiple agent files to tweak an instruction. One file, one responsibility.

### 2. Two Distinct Failure Paths
Most code generation pipelines only catch crashes. Ouroboros goes further:
- **Path 1** — Code crashes → error sent directly to Debugger
- **Path 2** — Code runs but logic is wrong → Tester diagnosis sent to Debugger

This distinction matters because a program can run perfectly and still be completely wrong.

### 3. Structured Tester Output
The Tester agent is prompted to reply in a strict format:
```
PASS: yes or no
REASON: one sentence explanation
```
This makes the response machine-parseable — the pipeline makes decisions based on `PASS`, not by trying to interpret free-form text.

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally

### 1. Clone the repository
```bash
git clone https://github.com/PritamAich/Ouroboros.git
cd Ouroboros
```

### 2. Pull the recommended model
```bash
ollama pull qwen2.5-coder:3b
```

> **Why `qwen2.5-coder:3b`?** It's purpose-built for code generation and runs comfortably within 8GB of available RAM. Larger models like Llama 3.1 8B or Mistral 7B require 16GB+ and are prone to crashing on consumer hardware.

### 3. Install dependencies
```bash
pip install requests
```

### 4. Run it
```bash
python main.py
```

---

## 🚀 Example Runs

**Simple task:**
```
Enter your task: Write a function that checks if a number is prime

✅ Code ran successfully. Testing logic...
✅ Logic check passed!

📝 Generated Code:
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(7))

📤 Output: True
```

**Self-healing in action:**
```
Enter your task: Write a function that finds the top 3 students by score

🔁 Attempt 1 of 3
✅ Code ran successfully. Testing logic...
⚠️  Logic check failed.
📝 Reason: Sorting is in ascending order — lowest scores are being selected, not highest.
🛠️  Fixing code...

🔁 Attempt 2 of 3
✅ Code ran successfully. Testing logic...
✅ Logic check passed!

📤 Output:
Frank: 100
Bob: 92
Eve: 90
```

---

## 🧪 What I Learned

### Prompt Engineering
Every rule added to a prompt is a direct instruction to the model. Through iterative testing, small additions like:
- *"All import statements must be at the top of the file, never inside functions"*
- *"Only fail if there is a CRITICAL logical problem, not a style issue"*
- *"Verify sorting direction when the task asks for highest or lowest values"*

...produced measurably better and more consistent outputs. Prompt engineering is less about creativity and more about precision.

### Multi-Agent Design
Splitting responsibilities across agents — rather than one giant prompt — makes the system debuggable. When something goes wrong, you know exactly which agent failed and why. Each agent has one job and one prompt.

### Local LLM Limitations
Smaller models (TinyLlama, base Phi, base Mistral) struggle with structured output and instruction-following. Model selection is itself an engineering decision — `qwen2.5-coder:3b` was chosen specifically because it's trained on code and follows structured prompts more reliably within tight RAM constraints.

---

## 🔮 Future Improvements

- [ ] **Streaming output** — show LLM responses token by token instead of waiting
- [ ] **Agent memory** — let the Debugger remember what fixes it already tried
- [ ] **Streamlit UI** — replace the terminal with a web interface for demos
- [ ] **Unit test generation** — have the Tester write and run actual unit tests instead of relying on LLM review
- [ ] **Claude API support** — optional switch from local Ollama to Anthropic's Claude API for higher quality outputs

---

## 👤 Author

**Pritam Aich** — built as a self-directed learning project exploring prompt engineering and agentic AI systems.

---

## 📄 License

MIT License — free to use, modify, and build on.
