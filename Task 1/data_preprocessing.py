import pandas as pd
import re
import string
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from keybert import KeyBERT
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize KeyBERT
kw_model = KeyBERT()

# Define product names and their variations
PRODUCT_MAP = {
    'ecobreeze': 'EcoBreeze AC',
    'vision': 'Vision LED TV',
    'photosnap': 'PhotoSnap Cam',
    'fitrun': 'FitRun Treadmill',
    'powermax': 'PowerMax Battery',
    'protab': 'ProTab X1',
    'smartwatch': 'SmartWatch V2',
    'soundwave': 'SoundWave 300',
    'ultraclean': 'UltraClean Vacuum',
    'robochef': 'RoboChef Blender'
}

# Define domain-specific stopwords
DOMAIN_STOPWORDS = {'order', 'number', 'support'}
STOPWORDS = set(stopwords.words('english')).union(DOMAIN_STOPWORDS)
lemmatizer = WordNetLemmatizer()

def clean_text_column(df, column='ticket_text'):
    """Clean text and normalize product names"""
    def process_text(text):
        if pd.isnull(text):
            return ""
        
        # Basic text cleaning
        text = text.lower()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Remove stopwords and lemmatize
        words = text.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in STOPWORDS]
        text = ' '.join(words)
        
        # Find and replace product names
        found_products = []
        text_lower = text.lower()
        
        # First look for exact matches
        for partial, full in sorted(PRODUCT_MAP.items(), key=len, reverse=True):
            if partial.lower() in text_lower:
                found_products.append((full, partial))
                # Remove the matched part to avoid double matching
                text = re.sub(r'\b' + re.escape(partial) + r'\b', '', text, flags=re.IGNORECASE)
        
        # Process each found product
        if found_products:
            words = text.split()
            final_words = []
            
            for word in words:
                word_added = False
                # Check if this word matches the last word of any product
                for full_name, partial in found_products:
                    last_word = full_name.split()[-1].lower()
                    if word.lower() == last_word.lower():
                        final_words.append(full_name)
                        word_added = True
                        found_products.remove((full_name, partial))
                        break
                if not word_added:
                    final_words.append(word)
            
            # Add any remaining products at the end
            if found_products:
                final_words.extend(full for full, _ in found_products)
            
            text = ' '.join(final_words)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    df[column] = df[column].astype(str).apply(process_text)
    return df

def normalize_product_names(df):
    """Normalize product names in product column"""
    def normalize_product(name):
        name = name.lower().strip()
        for partial, full in PRODUCT_MAP.items():
            if partial in name:
                return full
        return name.title()

    df['product'] = df['product'].astype(str).apply(normalize_product)
    return df

def load_data(file_path):
    """Load Excel file into a DataFrame"""
    return pd.read_excel(file_path)

def handle_missing_data(df):
    """Fill missing fields with empty strings"""
    df['issue_type'].fillna('', inplace=True)
    df['urgency_level'].fillna('', inplace=True)
    df['product'].fillna('', inplace=True)
    return df

def extract_keywords_for_issue_type(df):
    """Extract keywords for each issue type using KeyBERT"""
    issue_keywords = {}
    
    # Group texts by issue type (excluding empty ones)
    grouped_texts = df[df['issue_type'] != ''].groupby('issue_type')['ticket_text'].agg(list)
    
    for issue_type, texts in grouped_texts.items():
        # Join texts for this issue type
        combined_text = ' '.join(texts)
        
        # Extract keywords using KeyBERT
        keywords = kw_model.extract_keywords(combined_text, 
                                          keyphrase_ngram_range=(1, 3),
                                          stop_words='english',
                                          use_maxsum=True,
                                          nr_candidates=20,
                                          top_n=5)
        
        # Get just the keywords (not the scores)
        keywords = [k[0] for k in keywords]
        
        # Add common words from the texts
        all_words = ' '.join(texts).lower().split()
        filtered_words = [w for w in all_words if w not in STOPWORDS and len(w) > 3]
        common_words = [word for word, _ in Counter(filtered_words).most_common(10)]
        
        # Combine both keyword sources
        issue_keywords[issue_type] = list(set(keywords + common_words))
    
    # If we don't have any keywords yet (first run), use default categories
    if not issue_keywords:
        issue_keywords = {
            'Product Defect': ['stopped working', 'broken', 'malfunction', 'defect'],
            'Wrong Item': ['wrong product', 'order mixed', 'got wrong', 'received wrong'],
            'Installation Issue': ['setup fails', 'installation issue', 'install problem'],
            'Late Delivery': ['still not here', 'days late', 'not arrived', 'late delivery'],
            'Billing Problem': ['underbilled', 'charged', 'payment issue'],
            'General Inquiry': ['warranty', 'available in', 'tell me more'],
        }
    
    return issue_keywords

def infer_missing_values(df):
    """Infer issue_type and urgency_level using extracted keywords"""
    # Extract keywords from existing categorized tickets
    issue_keywords = extract_keywords_for_issue_type(df)
    
    print("\nExtracted keywords for each issue type:")
    for issue, keywords in issue_keywords.items():
        print(f"{issue}: {', '.join(keywords)}")
    
    # Use keywords to categorize remaining tickets
    for idx, row in df.iterrows():
        if row['issue_type'].strip() == '':
            # Score each issue type based on keyword matches
            scores = {}
            for issue_type, keywords in issue_keywords.items():
                score = sum(1 for kw in keywords if kw in row['ticket_text'].lower())
                scores[issue_type] = score
            
            # Assign the issue type with highest score (if any matches found)
            if any(scores.values()):
                best_match = max(scores.items(), key=lambda x: x[1])[0]
                df.at[idx, 'issue_type'] = best_match

        if row['urgency_level'].strip() == '':
            if 'no response' in row['ticket_text'] or 'contacted support' in row['ticket_text']:
                df.at[idx, 'urgency_level'] = 'High'
            elif 'late' in row['ticket_text']:
                df.at[idx, 'urgency_level'] = 'Medium'
            else:
                df.at[idx, 'urgency_level'] = 'Low'

    return df

def save_to_csv(df, original_path):
    """Save cleaned data to CSV with _cleaned suffix"""
    base = os.path.splitext(os.path.basename(original_path))[0]
    output_path = f"{base}_cleaned.csv"
    df.to_csv(output_path, index=False)
    return output_path

def preprocess_file(file_path):
    """Full preprocessing pipeline"""
    df = load_data(file_path)
    df = handle_missing_data(df)
    df = normalize_product_names(df)  # First normalize product column
    df = clean_text_column(df)  # Then clean and normalize text
    df = infer_missing_values(df)
    save_to_csv(df, file_path)
    return df

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python data_processing.py <path_to_xls_file>")
    else:
        preprocess_file(sys.argv[1])