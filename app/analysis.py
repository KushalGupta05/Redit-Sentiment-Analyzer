import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- IMPORTANT: NLTK Data Path Configuration ---
# Ensure NLTK can find its data.
# This path should point to where 'vader_lexicon' is (or will be) downloaded.
# It's set in app.py to ensure download before the app runs fully.
# The `nltk.data.path.append` ensures NLTK looks in the specified directory
# (e.g., a 'nltk_data' folder in the root of your project).
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))


# Initialize VADER SentimentIntensityAnalyzer
# This needs the 'vader_lexicon' data, which should be downloaded when the app starts.
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(posts):
    """
    Analyzes the sentiment of a list of text posts using NLTK's VADER.

    Args:
        posts (list): A list of dictionaries, where each dictionary has a
                      'content' key containing the text to analyze.

    Returns:
        list: A list of dictionaries, each containing the original 'title'
              and 'content', plus the calculated 'sentiment' (POSITIVE/NEGATIVE/NEUTRAL)
              and 'score' (VADER compound score).
    """
    results = []
    for post in posts:
        # Get sentiment scores using VADER's polarity_scores method
        # The 'compound' score is a normalized, weighted composite score.
        sentiment_score = sia.polarity_scores(post['content'])['compound']
        
        # Classify sentiment based on the compound score
        # VADER typically uses thresholds:
        # compound score >= 0.05 is positive
        # compound score <= -0.05 is negative
        # otherwise, it's neutral.
        if sentiment_score >= 0.05:
            sentiment = "POSITIVE"
        elif sentiment_score <= -0.05:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL" # Added Neutral sentiment for better classification
        
        # Append the analysis results to the list
        results.append({
            "title": post['title'],
            "content": post['content'],
            "sentiment": sentiment,
            "score": sentiment_score
        })
    return results
