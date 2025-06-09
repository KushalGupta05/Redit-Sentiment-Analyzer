import os
import matplotlib
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter
import re
import matplotlib.pyplot as plt
from flask import current_app
import nltk # Import nltk for stopwords

# Set Matplotlib backend to 'Agg' for non-interactive environments (like web servers)
matplotlib.use('Agg')

def create_directory(path):
    """
    Creates a directory if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")


def generate_graphs(sentiment_results, topic):
    """
    Generates a sentiment count bar chart and a word cloud from sentiment analysis results.
    The generated images are saved to static files and then encoded to base64.

    Args:
        sentiment_results (list): A list of dictionaries, each containing
                                  'sentiment', 'score', and 'content' keys.
        topic (str): The topic for which the analysis was performed, used in chart titles.

    Returns:
        tuple: A tuple containing two base64 encoded strings:
               (bar_chart_base64, word_cloud_base64).
               word_cloud_base64 might be None if no content is available.
    """
    # Extract sentiment labels from the results
    sentiments = [result['sentiment'] for result in sentiment_results]
    
    # Count the occurrences of each sentiment
    sentiment_counts = Counter(sentiments)
    sentiment_labels = list(sentiment_counts.keys())
    sentiment_values = list(sentiment_counts.values())

    # Define paths for saving images
    images_dir = os.path.join(current_app.instance_path, 'static', 'images')
    create_directory(images_dir)

    bar_chart_path = os.path.join(images_dir, 'sentiment_bar_chart.png')
    word_chart_path = os.path.join(images_dir, "word_cloud.png")

    # --- Generate Bar Chart (Sentiment Counts) ---
    plt.figure(figsize=(10, 6))
    # Create a bar plot of sentiment counts
    ax = sns.barplot(x=sentiment_labels, y=sentiment_values, palette='viridis') # Changed palette to 'viridis'
    plt.title(f'Distribution of Sentiments for Reddit Posts on "{topic}"', fontsize=16)
    plt.xlabel('Sentiment Category', fontsize=14)
    plt.ylabel('Number of Posts', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add count labels on top of each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center", va="center", fontsize=10, color='black',
                    xytext=(0, 5), textcoords='offset points')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(bar_chart_path)
    plt.close()

    bar_image_b64 = encode_image_to_base64(bar_chart_path)

    # --- Generate Word Cloud for Most Frequent Words ---
    text = ' '.join([result['content'] for result in sentiment_results if result['content'] and result['content'] != 'No Content Available'])

    text = re.sub(r'[^A-Za-z\s]', "", text.lower())
    words = text.split()
    
    # Filter out common English stop words and single-character words
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]

    word_counts = Counter(filtered_words)

    word_cloud_b64 = None

    if word_counts:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=200, colormap='viridis').generate_from_frequencies(word_counts)
        wordcloud.to_file(word_chart_path)
        word_cloud_b64 = encode_image_to_base64(word_chart_path)
    else:
        print("⚠️ Word cloud skipped: No meaningful words found in the content.")
    
    return bar_image_b64, word_cloud_b64


def encode_image_to_base64(image_path):
    """
    Encodes an image file to a base64 string.
    """
    with open(image_path, 'rb') as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
    return img_b64