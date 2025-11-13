import os
import sys
import pandas as pd


def main():
    print("==== START ====")

    # Define the path to the data_raw directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_raw_dir = os.path.abspath(os.path.join(current_dir, '..', 'data_raw'))
    reddit_data_dir = os.path.join(data_raw_dir, 'reddit_top_posts')

    # Check if the directory exists
    if not os.path.exists(reddit_data_dir):
        print(f"Directory not found: {reddit_data_dir}")
        sys.exit(1)
    print(f"Data directory found: {reddit_data_dir}")

    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(reddit_data_dir) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the directory.")
        sys.exit(1)
    print(f"Found {len(csv_files)} CSV files.")

    # Remove 50_subreddits_list.csv if it exists
    if '50_subreddits_list.csv' in csv_files:
        csv_files.remove('50_subreddits_list.csv')

    # Print the list of CSV files
    print("CSV files:")
    for file in csv_files:
        print(f"- {file}")

    for file in csv_files:
        file_path = os.path.join(reddit_data_dir, file)
        df = load_csv(file_path)
        if df is not None:
            print(f"First 5 rows of {file}:")
            print(df.head())

    print("==== END ====")

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {file_path} with shape {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

if __name__ == "__main__":
    main()