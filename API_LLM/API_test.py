import requests
from dotenv import load_dotenv
import os

load_dotenv()

generate_url = "http://127.0.0.1:8000/generate"
change_url = "http://127.0.0.1:8000/change"

headers = {
    "HeaderKey": os.getenv("API_KEY"), 
    "Content-Type": "application/json",
}

print("\n Enter your prompt bellow, press 'q' to exit !")

current_model = "llama3.2:latest"
print(f"\n Current model being used is: '{current_model}' if you want to change type 'ch model' !")

available_models = ["llama3.2:latest", "llama3.1:8b"]
print("\n Available LLM Models:")
for model in available_models:
    print(f"   - {model}")

while True:
    try:
        user_prompt = input("\nUser: ").strip()  # user input
        
        if user_prompt.lower() == 'q':  # press q or Q to quit
            print("\n Exiting... Goodbye!")
            break

        if user_prompt.lower() == 'ch model':  # change from 3.2 to 3.1 or vice versa
            
            response = requests.post(change_url, headers=headers)

            if response.status_code == 200: # if it was sucessfull
                current_model = response.json().get("message", "Unknown Model")
                print(f"\n Sucessfully changed to model {current_model}")
            else:
                print(f"\n ⚠ Error {response.status_code}: {response.text}")
                break
            
            continue 

        if not user_prompt: # if user didnt give an input
            print("\n ⚠︎ Error: Prompt cannot be empty!")
            continue  

        data = {"prompt": user_prompt} # user prompt is converted to json format

        response = requests.post(generate_url, json=data, headers=headers) # sends prompt and gets llm response

        if response.status_code == 200: # if it was sucessfull
            print(f"\nLLM ({current_model}): {response.json().get('response', 'No response received')}")
        else:
            print(f"\n ⚠︎ Error {response.status_code}: {response.text}")
            break

    except KeyboardInterrupt:
        print("\n Exiting... Goodbye!")
        break
    except Exception as e:
        print(f"\n ⚠︎ Unexpected error: {e} !")
        break


