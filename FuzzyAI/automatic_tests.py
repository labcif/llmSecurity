#python .\automatic_tests.py ollama/llama3.1:8b ollama/dolphin3:latest resources/10prompts.txt pt -> run this command to test this program

import subprocess
import time
import sys

def run_command(command: str):
    """runs a command and prints execution time"""
    start_time = time.time()
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n\n ------> Completed in {elapsed_time:.2f} seconds <------ \n")
    return process.returncode

def main():

    # ACRESCENTAR TEMPERATURA

    expected_args = 4  # expected args
    provided_args = len(sys.argv) - 1  # exclude script name

    if provided_args < expected_args:
        missing = expected_args - provided_args
        print(f"Error: Missing {missing} argument(s).")
    elif provided_args > expected_args:
        extra = provided_args - expected_args
        print(f"Error: {extra} extra argument(s) provided.")

    if provided_args != expected_args:
        print("\nCorrect Usage:")
        print("  python automatic_tests.py <PROVIDER/MODEL> <PROVIDER/UNCENSORED_MODEL> <PROMPTS_PATH>\n")
        print("  - PROVIDER/MODEL              -> ex: ollama/llama3.1:8b (LLM to attack)")
        print("  - PROVIDER/UNCENSORED_MODEL   -> ex: ollama/dolphin3:latest (helper LLM, we recommend an uncensored one)")
        print("  - PROMPTS_PATH                -> Path to file with prompts\n")
        print("  - LANGUAGE                    -> Attacking language (options: 'pt' for portuguese or 'en' for english)\n")
        print("ollama/qwen2.5 is needed to run this program\n")
        sys.exit(1)

    provider_model = sys.argv[1]
    uncensored_model = sys.argv[2]
    prompts_path = sys.argv[3]
    language = sys.argv[4]
    #temperature = sys.argv[5]

    print(f"Arguments received:")
    print(f" -> LLM to attack: {provider_model}")
    print(f" -> Uncensored LLM: {uncensored_model}")
    print(f" -> Prompts file: {prompts_path}\n")
    print(f" -> Language: {language}\n")
    
    # Activate Poetry

    #run_command("poetry shell") # -> uncomment this line, and comment the one bellow
    #_______________________________________________________________________________________________________________________________________
    run_command(r"C:\Users\franc\pipx\venvs\poetry\Scripts\activate")
    #_______________________________________________________________________________________________________________________________________

    cmd = f"python run.py -m {provider_model} -T {prompts_path} -N 100000"

    commands = [
        f"{cmd} -a shu -c sco",
        f"{cmd} -a bon -c obv",
        f"{cmd} -a wrd -c obv -x {uncensored_model} -e game_generation_model={uncensored_model} -l {language}",  # language sensitive
        f"{cmd} -a exp -c obv -l {language}",  # language sensitive
        f"{cmd} -a tax -c obv -x {uncensored_model} -e taxonomy_model={uncensored_model} -l {language}",  # language sensitive
        f"{cmd} -a per -c rat -x {uncensored_model} -e attack_model={uncensored_model} -e judge_model=ollama/qwen2.5:latest -x ollama/qwen2.5:latest -l {language}", # language sensitive
        f"{cmd} -a hal -c obv -x ollama/qwen2.5 -l {language}", # language sensitive
        f"{cmd} -a asc -c obv -x ollama/qwen2.5", 
        f"{cmd} -a dan -c obv -x ollama/qwen2.5 -l {language}", # language sensitive
        f"{cmd} -a crs -c obv -x ollama/qwen2.5 -e questions_generation_model=ollama/qwen2.5 -l {language}", # language sensitive
        #f"{cmd} -a act -c obv -x ollama/qwen2.5", # ? crash?
        f"{cmd} -a pst -c obv -x {uncensored_model} -cm ollama/qwen2.5 -e tag_extraction_model={uncensored_model} -l {language}", # language sensitive
        f"{cmd} -a pig -c obv -x {uncensored_model} -cm ollama/qwen2.5",
        f"{cmd} -a man -c obv -x {uncensored_model} -cm ollama/qwen2.5 -e question_placeholder=Question -e answer_placeholder=Response -e context_window=10000 -l {language}" # language sensitive
    ]
    
    total_start_time = time.time()

    for command in commands:
        if run_command(command) != 0:
            print(f"Error encountered during execution of command {command}\n")
            

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time

    print("=" * 50)
    print(f"All commands completed in {total_elapsed_time:.2f} seconds ({total_elapsed_time/60:.2f} minutes).")
    print("=" * 50)

if __name__ == "__main__":
    main()

