import os
import sys
import pandas as pd
import spacy
from collections import Counter
import json

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000 # Increase max length to handle large documents

def main():
    print("==== START ====")

    print("==== LOADING FILES ====")
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
    # print("CSV files:")
    # for file in csv_files:
    #     print(f"- {file}")

    # Iterate through each CSV file and load it into a DataFrame
    for file in csv_files[-17:]:
        file_path = os.path.join(reddit_data_dir, file)
        df = load_csv(file_path)
        if df is not None:
            print(f"==== ANALYZING {file} ====")
            analyze_data(df, file)

    print("==== END ====")

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # print(f"Loaded {file_path} with shape {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None
    
def analyze_data(df, file_name):
    # Example analysis: Print the first 5 rows of the DataFrame
    df['text'] = df['title'].fillna('') + ' ' + df['body'].fillna('')
    df['text_filtered'] = df['text'].apply(filter_stopwords)
    
    all_text = ' '.join(df['text_filtered'])
    
    # Calculate word frequencies
    words = all_text.split()
    word_counts = Counter(words)
    
    bigrams = get_ngrams(all_text, 2)
    trigrams = get_ngrams(all_text, 3)
    
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)
    
    # Perform POS tagging and count POS tags
    doc = nlp(all_text)
    pos_counts = Counter([token.pos_ for token in doc])
    
    # Calculate POS tag ratios
    total_tokens = len(doc)
    pos_ratios = {pos: count / total_tokens for pos, count in pos_counts.items()}
    
    # Categorize words by POS tag
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    verbs = [token.text for token in doc if token.pos_ == 'VERB']
    adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
    adverbs = [token.text for token in doc if token.pos_ == 'ADV']
    
    # Count word frequencies per category
    noun_counts = Counter(nouns)
    verb_counts = Counter(verbs)
    adjective_counts = Counter(adjectives)
    adverb_counts = Counter(adverbs)
    
    # Calculate word length distributions
    noun_lengths = Counter([len(word) for word in nouns])
    verb_lengths = Counter([len(word) for word in verbs])
    adjective_lengths = Counter([len(word) for word in adjectives])
    adverb_lengths = Counter([len(word) for word in adverbs])
    
    print("Most common bigrams:")
    print(bigram_counts.most_common(10))
    
    print("Most common trigrams:")
    print(trigram_counts.most_common(10))

    # Structure the results in a dictionary
    results = {
        "pos_ratios": pos_ratios,
        "word_length_distributions": {
            "nouns": dict(sorted(noun_lengths.items())),
            "verbs": dict(sorted(verb_lengths.items())),
            "adjectives": dict(sorted(adjective_lengths.items())),
            "adverbs": dict(sorted(adverb_lengths.items()))
        },
        "most_common_words": {word: count for word, count in word_counts.most_common(30)},
        "most_common_nouns": {word: count for word, count in noun_counts.most_common(30)},
        "most_common_verbs": {word: count for word, count in verb_counts.most_common(30)},
        "most_common_adjectives": {word: count for word, count in adjective_counts.most_common(30)},
        "most_common_adverbs": {word: count for word, count in adverb_counts.most_common(30)},
        "most_common_bigrams": {bigram: count for bigram, count in bigram_counts.most_common(10)},
        "most_common_trigrams": {trigram: count for trigram, count in trigram_counts.most_common(10)},
    }

    # Save the results to a file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_processed_dir = os.path.abspath(os.path.join(current_dir, '..', 'static/data_processed'))
    if not os.path.exists(data_processed_dir):
        os.makedirs(data_processed_dir)
        
    output_file_path = os.path.join(data_processed_dir, f"{file_name.replace('.csv', '')}_analysis.json")
    with open(output_file_path, 'w') as f:
        json.dump(results, f, indent=4)
    
def filter_stopwords(text):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha and len(token.text) > 2]
    return " ".join(tokens)

def get_ngrams(text, n):
    tokens = text.split()
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

if __name__ == "__main__":
    main()