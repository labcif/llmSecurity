import json
from deep_translator import GoogleTranslator

# File paths
input_file = 'llama2-uncensored-prompt-response-t0.jsonl'
output_file = 'llama2-uncensored-prompt-response-t0-portuguese.jsonl'

# Translator
translator = GoogleTranslator(source='auto', target='pt')

# Translate each line
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        data = json.loads(line)
        
        # Translate common fields if they exist
        for key in ['prompt', 'response', 'instruction', 'input', 'output']:
            if key in data and isinstance(data[key], str):
                try:
                    data[key] = translator.translate(data[key])
                except Exception as e:
                    print(f"Translation error on key '{key}': {e}")
        
        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

print("Translation completed. Output saved to:", output_file)
