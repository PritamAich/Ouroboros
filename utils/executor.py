import subprocess

def run_code(file_path):
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5
        )

        return result.stdout, result.stderr

    except Exception as e:
        return "", str(e)