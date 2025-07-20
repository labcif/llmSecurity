import subprocess
from itertools import product

script_path = "automatic_args_handler.py"

models = ["ollama/mistral:latest", "ollama/llama3.1:8b", "ollama/aya:8b"]
temperatures = [0.2, 0.8, None]
top_ps = [0.1, 0.9, None]
langs = ["en", "pt"]

for model in models:
    for temp, top_p in product(temperatures, top_ps):
        if temp is not None and top_p is not None:
            continue
        for lang in langs:
            if lang == "en":
                prompts_path = "./resources/10prompts_en.txt"
            elif lang == "pt":
                prompts_path = "./resources/10prompts.txt"
            else:
                continue

            args = [model, "ollama/dolphin3:latest", prompts_path, lang]

            if temp is not None:
                args += ["--temperature", str(temp)]
            if top_p is not None:
                args += ["--top_p", str(top_p)]

            print(f"\nRunning with model={model} temp={temp} top_p={top_p} lang={lang}\n")
            command = ["python", script_path] + args
            subprocess.run(command)
