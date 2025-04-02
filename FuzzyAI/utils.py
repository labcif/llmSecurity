import subprocess


def run_ollama_list_command():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error running 'ollama list': {result.stderr}")
        return
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Please make sure to download ollama from ollama.com")
        return
    except Exception as e:
        print(f"An error occurred while running 'ollama list': {e}")
        return
    
def get_ollama_models() -> list[str]:
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running 'ollama list': {result.stderr}")
            return []
        
        lines = result.stdout.splitlines()
        models = [line.split()[0] for line in lines[1:] if line.strip()]
        return models
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Please make sure to download ollama from ollama.com")
        return []
    except Exception as e:
        print(f"An error occurred while running 'ollama list': {e}")
        return []