#python .\automatic_tests.py ollama/mistral:latest ollama/dolphin3:latest resources/10prompts.txt pt temp topp -> run this command to test this program

import subprocess
import time
import argparse

def run_command(command: str):
    """Runs a command and prints execution time."""
    start_time = time.time()
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n\n ------> Completed in {elapsed_time:.2f} seconds <------ \n")
    return process.returncode

def main():
    parser = argparse.ArgumentParser(
        description="Run automated fuzzing attacks with specified models and parameters."
    )

    parser.add_argument("model", help="LLM to attack, e.g., ollama/llama3.1:8b")
    parser.add_argument("uncensored_model", help="Uncensored LLM helper, e.g., ollama/dolphin3:latest")
    parser.add_argument("prompts_path", help="Path to the file with prompts")
    parser.add_argument("language", choices=["pt", "en"], help="Language to attack (pt or en)")

    parser.add_argument("--temperature", "-tm", type=float, default=None, help="LLM response randomness (optional)")
    parser.add_argument("--top_p", "-tp", type=float, default=None, help="Top-p nucleus sampling value (optional)")

    args = parser.parse_args()

    print(f"Arguments received:")
    print(f" -> LLM to attack: {args.model}")
    print(f" -> Uncensored LLM: {args.uncensored_model}")
    print(f" -> Prompts file: {args.prompts_path}")
    print(f" -> Language: {args.language}")
    print(f" -> Temperature: {args.temperature}")
    print(f" -> Top_p: {args.top_p}\n")

    # Activate Poetry (adjust as needed)
    run_command("poetry shell")

    cmd = f"python run.py -m {args.model} -T {args.prompts_path} -N 10000000"

    # Top_p and Temperature optional 
    optional_args = ""
    if args.temperature is not None:
        optional_args += f" -tm {args.temperature}"
    if args.top_p is not None:
        optional_args += f" -tp {args.top_p}"

    commands = [
        f"{cmd}{optional_args} -a shu -c sco",
        f"{cmd}{optional_args} -a bon -c obv",
        f"{cmd}{optional_args} -a wrd -c obv -x ollama/qwen2.5 -e game_generation_model=ollama/qwen2.5 -l {args.language}",
        f"{cmd}{optional_args} -a exp -c obv -l {args.language}",
        f"{cmd}{optional_args} -a tax -c obv -x {args.uncensored_model} -e taxonomy_model={args.uncensored_model} -l {args.language}",
        f"{cmd} -a per -c rat -x {args.uncensored_model} -e attack_model={args.uncensored_model} -e judge_model=ollama/qwen2.5:latest -x ollama/qwen2.5:latest -l {args.language}",
        f"{cmd}{optional_args} -a hal -c obv -x ollama/qwen2.5 -l {args.language}",
        f"{cmd}{optional_args} -a asc -c obv -x ollama/qwen2.5",
        f"{cmd}{optional_args} -a dan -c obv -x ollama/qwen2.5 -l {args.language}",
        f"{cmd}{optional_args} -a crs -c obv -x ollama/qwen2.5 -e questions_generation_model=ollama/qwen2.5 -l {args.language}",
        f"{cmd}{optional_args} -a vgr -c obv -l {args.language}",
        f"{cmd}{optional_args} -a pst -c obv -x {args.uncensored_model} -cm ollama/qwen2.5 -e tag_extraction_model={args.uncensored_model} -l {args.language}",
        f"{cmd}{optional_args} -a pig -c obv -x {args.uncensored_model} -cm ollama/qwen2.5",
        f"{cmd}{optional_args} -a man -c obv -x {args.uncensored_model} -cm ollama/qwen2.5 -e question_placeholder=Question -e answer_placeholder=Response -e context_window=1000000 -l {args.language}"
    ]


    total_start_time = time.time()

    for command in commands:
        if run_command(command) != 0:
            print(f"Error encountered during execution of command:\n{command}\n")

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time

    print("=" * 50)
    print(f"All commands completed in {total_elapsed_time:.2f} seconds ({total_elapsed_time/60:.2f} minutes).")
    print("=" * 50)

if __name__ == "__main__":
    main()
