import os
import json
import requests
import datetime
import csv

def add_metadata_to_analysis(file_path, subreddit_name, metadata_list):
    try:
        # Load existing analysis data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fetch subreddit metadata from Reddit API
        url = f'https://www.reddit.com/r/{subreddit_name}/about.json'
        headers = {'User-Agent': 'subreddit-metadata-fetcher/1.0'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data for r/{subreddit_name}: HTTP {response.status_code}")
            return

        info = response.json()['data']

        # Add metadata fields
        data['display_name'] = info.get('display_name')
        data['subscribers'] = info.get('subscribers')
        data['description'] = info.get('public_description', '')
        data['created_date'] = datetime.datetime.fromtimestamp(info['created_utc']).strftime('%Y-%m-%d')

        # Save updated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Collect metadata for CSV
        metadata_list.append({
            'name': subreddit_name,
            'display_name': info.get('display_name'),
            'subscribers': info.get('subscribers'),
            'description': info.get('public_description', ''),
            'created_date': datetime.datetime.fromtimestamp(info['created_utc']).strftime('%Y-%m-%d')
        })

        print(f"Updated {file_path} with metadata for r/{subreddit_name}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    data_dir = 'static/data_processed'
    metadata_list = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith('_analysis.json'):
            subreddit_name = file_name.replace('_analysis.json', '')
            file_path = os.path.join(data_dir, file_name)
            add_metadata_to_analysis(file_path, subreddit_name, metadata_list)

    # Write metadata to CSV
    csv_file = 'data_analysis/subreddits_metadata.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'display_name', 'subscribers', 'description', 'created_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_list)

    print(f"Metadata CSV created at {csv_file}")

if __name__ == '__main__':
    main()