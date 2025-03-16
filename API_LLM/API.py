# python -m uvicorn API:app --reload -> command to run API

from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# pydantic model for API requests
class PromptRequest(BaseModel):
    prompt: str
    #temperature: float = 0.0 # ensures a predictable and consistente response

load_dotenv()  # loads value from environment file (stored API key)
N_CREDITS = 1000000 # high number to test with prompts extracted from datasets

API_KEY= os.getenv("API_KEY") # fetches the API_KEY 
if not API_KEY:
    raise ValueError("API_KEY is missing from environment variables!")

API_KEY_CREDITS = {API_KEY: N_CREDITS} # assigns 'N_CREDITS' credits to API_KEY (number of times a key can be used)
print(API_KEY_CREDITS) 

app = FastAPI() # initializes FastAPI app, and allows to define routes

current_model = "llama3.1:8b" # acts as default

def verify_api_key(HeaderKey: str = Header(None)): # HeaderKey is extracted from the headers in HTTP requests
    
    if not HeaderKey:
        raise HTTPException(status_code=401, detail="API Key is missing!") # raises 401 (Unauthorized) error if the key is invalid
    
    credits = API_KEY_CREDITS.get(HeaderKey, 0)
    if credits <= 0:
        raise HTTPException(status_code=403, detail="Out of credits!") # raises 403 error if no credits are left

    return HeaderKey

@app.post("/change") # route to change llama model being used
def change_model(HeaderKey: str = Depends(verify_api_key)):
    global current_model  

    # toggle model selection
    if current_model == "llama3.1:8b":
        current_model = "dolphin3:latest"
    else:
        current_model = "llama3.1:8b"

    return {"message": {current_model}}

@app.post("/generate") # route to generate LLM response
def generate(request: PromptRequest, HeaderKey: str = Depends(verify_api_key)):
    API_KEY_CREDITS[HeaderKey] -= 1 # after verification decrements one credit

    try: # try except block is used in order for the API not to crash if ollama.chat fails

        response = ollama.chat(  # calls the LLM model 
            model=current_model, 
            messages=[{"role": "user", "content": request.prompt}],
            options={"temperature": 0, "top_p": 0} # temperature and top_p are always 0 which ensures a predictable and consistente response
        )  
        return {"response": response["message"]["content"]} # returns LLM response to previous sent prompt, in JSON format
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       