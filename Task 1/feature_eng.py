import pandas as pd
import numpy as np
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import text2emotion as t2e
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Download required NLTK data
nltk.download('punkt', quiet=True)
analyzer = SentimentIntensityAnalyzer()

PRODUCT_LIST = [
    "RoboChef Blender", "Vision LED TV", "PhotoSnap Cam", "FitRun Treadmill",
    "PowerMax Battery", "EcoBreeze AC", "ProTab X1", "SmartWatch V2",
    "SoundWave 300", "UltraClean Vacuum"
]

PRODUCT_COUNTS = {
    "RoboChef Blender": 116,
    "Vision LED TV": 109,
    "PhotoSnap Cam": 103,
    "FitRun Treadmill": 102,
    "PowerMax Battery": 102,
    "EcoBreeze AC": 100,
    "ProTab X1": 99,
    "SmartWatch V2": 95,
    "SoundWave 300": 90,
    "UltraClean Vacuum": 84
}

ISSUE_COUNTS = {
    "Billing Problem": 146,
    "General Inquiry": 146,
    "Account Access": 143,
    "Installation Issue": 142,
    "Product Defect": 121,
    "Wrong Item": 114,
    "Late Delivery": 112
}

URGENCY_MAP = {'Low': 1, 'Medium': 2, 'High': 3}
URGENCY_WORDS = {
    'urgent': 3,
    'immediately': 2,
    'critical': 3,
    'asap': 3,
    'emergency': 3,
    'crucial': 2,
    'priority': 2
}

COLORS = ['white', 'black', 'red', 'blue', 'green', 'silver', 'grey', 'gold']

def load_data(file_path):
    """Load data and ensure all required columns exist"""
    df = pd.read_csv(file_path)
    required_cols = ['ticket_text', 'issue_type', 'urgency_level', 'product']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    return df

def get_sentiment(text):
    """Get VADER sentiment scores with error handling"""
    try:
        return analyzer.polarity_scores(str(text))['compound']
    except:
        return 0

def get_emotions(text):
    """Get emotion scores with error handling"""
    try:
        emotions = t2e.get_emotion(str(text))
        return pd.Series(emotions)
    except:
        return pd.Series({
            'Happy': 0, 'Angry': 0, 'Surprise': 0, 'Sad': 0, 'Fear': 0
        })

def extract_basic_features(df):
    """Extract basic text features"""
    df['ticket_length'] = df['ticket_text'].apply(lambda x: len(str(x).split()))
    df['char_count'] = df['ticket_text'].apply(lambda x: len(str(x)))
    df['exclamation_count'] = df['ticket_text'].apply(lambda x: str(x).count('!'))
    df['question_count'] = df['ticket_text'].apply(lambda x: str(x).count('?'))
    df['uppercase_ratio'] = df['ticket_text'].apply(
        lambda x: sum(1 for c in str(x) if c.isupper()) / len(str(x)) if len(str(x)) > 0 else 0
    )
    return df

def add_tfidf_features(df):
    """Add TF-IDF based features"""
    print("Generating TF-IDF features...")
    tfidf = TfidfVectorizer(max_features=50, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['ticket_text'].fillna(''))
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=[f'tfidf_{f}' for f in tfidf.get_feature_names_out()]
    )
    return pd.concat([df, tfidf_df], axis=1)

def extract_sentiment_emotion(df):
    """Extract sentiment and emotion features"""
    print("Analyzing sentiment and emotions...")
    df['sentiment_score'] = df['ticket_text'].apply(get_sentiment)
    emotions = df['ticket_text'].apply(get_emotions)
    df = pd.concat([df, emotions.add_prefix('emotion_')], axis=1)
    return df

def extract_problem_duration(text):
    """Extract duration mentioned in text"""
    duration_patterns = {
        'day': 1,
        'week': 7,
        'month': 30,
        'hour': 1/24
    }
    total_days = 0
    text = str(text).lower()
    
    for unit, multiplier in duration_patterns.items():
        matches = re.finditer(r'(\d+)\s*' + unit + 's?', text)
        for match in matches:
            total_days += int(match.group(1)) * multiplier
    
    return total_days

def extract_monetary_mention(text):
    """Extract monetary values mentioned"""
    text = str(text).lower()
    amounts = re.findall(r'\$?\s*(\d+(?:\.\d{2})?)\s*(?:dollars?|usd|\$)?', text)
    return sum(float(amt) for amt in amounts) if amounts else 0

def detect_escalation(text):
    """Detect escalation signals in text"""
    text = str(text).lower()
    escalation_patterns = [
        r'contacted\s+support',
        r'called\s+(\d+\s+)?times?',
        r'emailed\s+(\d+\s+)?times?',
        r'multiple\s+attempts?',
        r'again\s+and\s+again',
        r'still\s+waiting',
        r'no\s+response',
        r'escalate'
    ]
    return sum(bool(re.search(pattern, text)) for pattern in escalation_patterns)

def urgency_lexicon_count(text):
    """Calculate weighted urgency score based on urgency words"""
    text = str(text).lower()
    return sum(weight for word, weight in URGENCY_WORDS.items() if word in text)

def adjust_urgency(df):
    """Adjust urgency levels based on various factors"""
    print("Adjusting urgency levels...")
    
    # Handle empty text cases first
    mask_empty = (df['ticket_text'].str.strip() == '') & \
                (df['issue_type'].isin([
                    'Billing Problem', 'Account Access',
                    'Installation Issue', 'Wrong Item',
                    'Late Delivery'
                ]))
    df.loc[mask_empty, 'urgency_level'] = 'Low'
    
    # Handle support contact cases
    mask_contact = df['ticket_text'].str.contains(
        r'contacted support|called|reached out',
        regex=True,
        na=False
    )
    
    # Upgrade non-High urgency levels
    df.loc[mask_contact & (df['urgency_level'] != 'High'), 'urgency_level'] = \
        df.loc[mask_contact & (df['urgency_level'] != 'High'), 'urgency_level'].map({
            'Low': 'Medium',
            'Medium': 'High'
        })
    
    return df

def compute_priority_score(df):
    """Compute final priority score"""
    df['priority_score'] = (
        df['urgency_level'].map(URGENCY_MAP) +
        (df['exclamation_count'] > 0).astype(int) +
        (df['escalation_signal'] > 1).astype(int) +
        (df['sentiment_score'] < -0.5).astype(int)
    )
    return df

def extract_contextual_features(df):
    """Extract all contextual features"""
    print("Extracting contextual features...")
    df['problem_duration_days'] = df['ticket_text'].apply(extract_problem_duration)
    df['monetary_value'] = df['ticket_text'].apply(extract_monetary_mention)
    df['escalation_signal'] = df['ticket_text'].apply(detect_escalation)
    df['urgency_word_score'] = df['ticket_text'].apply(urgency_lexicon_count)
    df['has_repeated_contact'] = df['ticket_text'].apply(
        lambda x: bool(re.search(r'contacted .*(twice|again|times)', str(x), re.I))
    )
    return df

def analyze_product_issues(df):
    """Analyze issues by product"""
    print("\n📊 Product Issue Analysis:")
    issues = {}
    
    for product in PRODUCT_LIST:
        prod_df = df[df['product'] == product]
        
        # Get issue distribution
        issue_dist = prod_df['issue_type'].value_counts()
        
        # Get common words
        vectorizer = CountVectorizer(stop_words='english', max_features=10)
        if len(prod_df) > 0:
            matrix = vectorizer.fit_transform(prod_df['ticket_text'].fillna(''))
            words = vectorizer.get_feature_names_out()
        else:
            words = []
            
        # Calculate average sentiment
        avg_sentiment = prod_df['sentiment_score'].mean()
        
        issues[product] = {
            'total_tickets': len(prod_df),
            'main_issue': issue_dist.index[0] if len(issue_dist) > 0 else 'No issues',
            'issue_count': issue_dist.iloc[0] if len(issue_dist) > 0 else 0,
            'common_words': list(words),
            'avg_sentiment': avg_sentiment
        }
        
        print(f"\n{product}:")
        print(f"- Main issue: {issues[product]['main_issue']} ({issues[product]['issue_count']} tickets)")
        print(f"- Common words: {', '.join(issues[product]['common_words'])}")
        print(f"- Average sentiment: {avg_sentiment:.2f}")
    
    return issues

def analyze_color_preferences(df):
    """Analyze color preferences in general inquiries"""
    print("\n🎨 Color Preference Analysis:")
    color_mentions = defaultdict(lambda: defaultdict(int))
    
    inquiries = df[df['issue_type'] == 'General Inquiry']
    for _, row in inquiries.iterrows():
        text = str(row['ticket_text']).lower()
        product = row['product']
        for color in COLORS:
            if color in text:
                color_mentions[product][color] += 1
    
    for product in color_mentions:
        if color_mentions[product]:
            print(f"\n{product}:")
            for color, count in sorted(color_mentions[product].items(), 
                                    key=lambda x: x[1], reverse=True):
                print(f"- {color}: {count}")
    
    return dict(color_mentions)

def print_summary_stats(df):
    """Print summary statistics"""
    print("\n📈 Summary Statistics:")
    
    print("\nIssue Type Distribution:")
    print(df['issue_type'].value_counts())
    
    print("\nUrgency Level Distribution:")
    print(df['urgency_level'].value_counts())
    
    print("\nAverage Sentiment by Issue Type:")
    print(df.groupby('issue_type')['sentiment_score'].mean().round(3))
    
    print("\nMost Common Urgent Products:")
    print(df[df['urgency_level'] == 'High']['product'].value_counts().head())
    
    print("\nProducts with Most Negative Sentiment:")
    print(df.groupby('product')['sentiment_score'].mean().sort_values().head())

def run_feature_engineering(file_path):
    """Run the complete feature engineering pipeline"""
    print("Loading data...")
    df = load_data(file_path)
    
    # Store original columns
    original_columns = df.columns.tolist()
    
    # Extract all features
    df = extract_basic_features(df)
    df = extract_sentiment_emotion(df)
    df = extract_contextual_features(df)
    df = add_tfidf_features(df)
    df = adjust_urgency(df)
    df = compute_priority_score(df)
    
    # Run analyses
    product_issues = analyze_product_issues(df)
    color_prefs = analyze_color_preferences(df)
    print_summary_stats(df)
    
    # Select columns for output
    columns_to_keep = original_columns + [
        'ticket_length',
        'char_count',
        'sentiment_score',
        'monetary_value',
        'priority_score'
    ]
    
    output_df = df[columns_to_keep]
    
    # Save enhanced dataset
    output_path = file_path.replace('.csv', '_enhanced_features.csv')
    output_df.to_csv(output_path, index=False)
    print(f"\n✅ Enhanced feature data saved to: {output_path}")
    print(f"Columns in output file: {', '.join(output_df.columns)}")
    
    return df, product_issues, color_prefs

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python enhanced_feature_eng.py <cleaned_csv_file>")
    else:
        run_feature_engineering(sys.argv[1]) 