import json
import os

# Example usage
input_jsonl_file = 'datasets/prompts.jsonl'  # Ensure this path is correct
output_json_folder = 'datasets'  # Change if needed

print(f"Checking file: {os.path.abspath(input_jsonl_file)}")
print(f"File exists? {os.path.exists(input_jsonl_file)}")

def convert_jsonl_to_json(input_jsonl_file, output_json_folder):
    # Ensure the output folder exists
    os.makedirs(output_json_folder, exist_ok=True)
    
    # Determine the output JSON filename
    base_name = os.path.splitext(os.path.basename(input_jsonl_file))[0]
    output_json_file = os.path.join(output_json_folder, base_name + '.json')
    
    # Read the JSONL file and aggregate the data
    data = []
    try:
        with open(input_jsonl_file, 'r', encoding='utf-8') as jsonl_file:
            for line_number, line in enumerate(jsonl_file, start=1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"❌ Error decoding JSON on line {line_number}: {e}")
                    continue
        
        # Write to the JSON file
        with open(output_json_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        
        print(f"✅ Converted {input_jsonl_file} to {output_json_file}")
    except FileNotFoundError:
        print(f"❌ File not found: {input_jsonl_file}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")



convert_jsonl_to_json(input_jsonl_file, output_json_folder)
