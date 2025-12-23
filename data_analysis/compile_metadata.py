import os
import json

def compile_metadata(data_dir, output_file):
    metadata = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith('_analysis.json'):
            subreddit_name = file_name.replace('_analysis.json', '')
            file_path = os.path.join(data_dir, file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Extract metadata fields
                metadata[subreddit_name] = {
                    'display_name': data.get('display_name'),
                    'subscribers': data.get('subscribers'),
                    'description': data.get('description'),
                    'created_date': data.get('created_date')
                }

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Save compiled metadata to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Compiled metadata saved to {output_file}")

def main():
    data_dir = 'static/data_processed'
    output_file = 'static/data_processed/all_subreddit_metadata.json'
    compile_metadata(data_dir, output_file)

if __name__ == '__main__':
    main()