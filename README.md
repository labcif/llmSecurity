# LLM-Security: An Automated Pipeline for Adversarial Robustness Testing

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-31210/)


This repository contains the complete codebase for **"Cybersecurity in LLMs: Exploration of Vulnerabilities,"** a research project from the Instituto Politécnico de Leiria.

The project presents a comprehensive, automated pipeline designed to evaluate the security and robustness of locally executed Large Language Models (LLMs). It systematically applies large-scale adversarial attacks to identify and analyze vulnerabilities.

## Core Features

* **Automated Security Pipeline:** An end-to-end system for executing attacks, parameterizing tests, collecting metrics, and classifying results;
* **Local LLM Testing:** Natively supports models running via [Ollama](https://ollama.com/), allowing for secure, cost-effective testing without API dependencies;
* **Systematic Adversarial Attacks:** Deploys 14 distinct types of adversarial *jailbreak* attacks, from simple prompt obfuscation to complex, multi-turn scenarios;
* **Dynamic Parameter Testing:** Automatically tests the impact of `temperature` and `top_p` parameters on model robustness;
* **Multilingual Evaluation:** Capable of running identical attacks in both **English** and **Portuguese** to assess multilingual security consistency;
* **Automated Results Classification:** Employs an auxiliary LLM (Qwen3) to automatically classify attack responses as successful jailbreaks (`V`) or safe refusals (`X`);
* **Comprehensive Data Aggregation:** All test results, metrics, parameters, and classifications are automatically compiled into a single, structured Excel file for analysis;
* **Automated Visualization:** Includes scripts to parse the final data file and generate statistical graphs for analysis;

---

## Technical Architecture & Pipeline

The system is orchestrated by a series of custom Python scripts that manage the entire testing lifecycle:

1.  **`automatic_tests.py`:** The main entry point. It iterates through all defined test combinations (`Model`, `Language`, `temperature`, `top_p`, (...) ).
2.  **`automatic_args_handler.py`:** This script receives parameters from the main test runner and constructs the precise execution commands for the fuzzer.
3.  **FuzzyAI Fuzzer (Modified):** The core testing engine. It takes the commands, applies the specified adversarial attack to the target prompts, and queries the local LLM via Ollama.
4.  **Metric Generation:** The modified fuzzer exports detailed metrics for each attack run into a dedicated Excel file, logging the prompt, response, parameters, and execution time.
5.  **Automated Classification:** After tests are complete, the `verify_jailbreaks_local.py` script runs. It reads the generated Excel files and uses an auxiliary LLM (Qwen3) to evaluate each prompt-response pair for jailbreaks.
6.  **Data Compilation:** A final script aggregates all individual test results from their respective directories into one master Excel file.
7.  **Graph Generation:** Analytics scripts process the master file to create the final graphs and visualizations seen in the report.

<img width="1333" height="818" alt="Test Automation Scripts" src="https://github.com/user-attachments/assets/3eddd81e-4d00-4e7c-8eae-39e7520d300c" />

---

## Key Modifications & Contributions

This project is built on the [cyberark/FuzzyAI Fuzzer](https://github.com/cyberark/FuzzyAI), but includes substantial modifications to enhance its capabilities for systematic research.

* **New Attack: Videogame Roleplay:** Implemented a novel attack vector (`vgr`) that frames malicious requests within a fictitious videogame scenario to bypass ethical guardrails.
* **Improved Attack: Crescendo:** Heavily modified the existing `crs` attack to improve its logic and effectiveness.
* **Multilingual Support:** Refactored attack handlers and classifiers to support non-English languages, with full support for Portuguese added.
* **Dynamic Parameterization:** Added command-line arguments and handler logic to control the `temperature` and `top_p` of the target LLM for each test run.
* **Enhanced Data Export:** Built a new module to automatically export all attack metrics (prompt, response, runtime, params, etc.) to a structured Excel file.
* **Robust File & Directory Handling:**
    * Fixed ASCII/UTF-8 encoding bugs to correctly process non-English characters.
    * Implemented a logical directory structure to automatically save results in organized folders (`results/<model>/<attack>__<lang>__<timestamp>`).
* **Expanded Token Limit:** Increased the hard-coded token limit from 100 to 100,000 to prevent premature truncation of model responses.

---

## Models & Attacks Tested

### Models
This study evaluated three popular open-source models, all executed locally via Ollama:
* **LLaMA3.1:8B** (Meta AI)
* **Mistral: 7B** (Mistral AI)
* **Aya:8B** (Cohere AI)

### Adversarial Attacks
A total of 14 distinct attack techniques were selected and applied:

| Attack Name | Abbreviation | Description | 
| :--- | :--- | :--- |
| ASCII Smuggling | `asc` | Embeds hidden instructions using invisible Unicode Tags, which LLMs can process, posing a prompt injection risk. Filtering these tags is crucial to prevent exploitation |
| Best of N | `bon` | Exploits prompt augmentations to elicit harmful responses from AI models across modalities, achieving high success rates with repeated sampling |
| Crescendo | `crs` | Engaging the model in a series of escalating conversational turns, starting with innocuous queries and gradually steering the dialogue toward restricted or sensitive topics |
| Do Anything Now (DAN) | `dan` | Promotes the LLM to adopt an unrestricted persona that ignores standard content filters, allowing it to "Do Anything Now" |
| Thought Experiment | `exp` | Modifies the prompt by adding a thought experiment-related prefix and precautions implemented suffix |
| Hallucinations | `hal` | Uses Hallucinations to Bypass RLHF Filters |
| Many-shot Prompting | `man` | Exploits large context windows in language models by embedding multiple fake dialogue examples, gradually weakening the model's safety responses |
| Paraphraser | `per` | Automates the generation of adversarial prompts by pairing two LLMs (“attacker” and “target”) to iteratively refine prompts until achieving jailbreak |
| Pig Latin | `pig` | Structural attack that works by altering the surface-level structure of the text without changing its underlying meaning |  
| Videogame Roleplay | `vgr` | Wraps a adversarial prompt with a specific prefix and suffix related to videogames, this narrative framing is designed to induce the model to suspend its normal security filters, treating the interaction as a harmless, fictional simulation | 
| Back to the Past | `pst` | Modifies the prompt by adding a profession-based prefix and a past related suffix | 
| Shuffle Inconsistency | `shu` | Shuffles harmful prompts to bypass safety while remaining comprehensible to the LLM | 
| Taxonomy | `tax` | Uses persuasive language techniques like emotional appeal and social proof to jailbreak LLMs | 
| Word Game | `wrd` | Disguises harmful prompts as word puzzles | 

---

## Summary of Findings

* **Model Vulnerability:** `aya:8b` was found to be the most vulnerable model, with a jailbreak success rate +9.0% above the average. `llama3.1:8b` was the most robust, with a success rate -9.5% below the average.
* **Model Performance:** `mistral:7b` was the fastest model, performing tests ~88 seconds faster than the average.`aya:8b` was the slowest, running ~162 seconds slower than the average.
* **Language Impact:** The choice of language (EN vs. PT) had a negligible impact on the *success rate* of attacks. However, it had a significant impact on *execution time*, with Portuguese tests running ~28 seconds slower on average.
* **Parameter Impact:** `temperature` and `top_p` values had a marginal effect on attack success rates.
* **Attack Efficacy:** The `dan` (Do Anything Now), `man` (Many-shot), and `crs` (Crescendo) attacks were consistently the most effective at jailbreaking the tested models.



This project was developed as part of the "Projeto Informático" (Final Bachelor Project) at the Escola Superior de Tecnologia e Gestão, Instituto Politécnico de Leiria (ESTG-IPL).
