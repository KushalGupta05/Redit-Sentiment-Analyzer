from flask import Blueprint, request, jsonify, render_template, current_app
from app.fetch_reddit_data import fetch_reddit_data
from app.analysis import analyze_sentiment
from app.graphs import generate_graphs
from app import db, cache
from app.models import SentimentAnalysis
from app.logger import configure_logger # Ensure this import is correct

# Create a Blueprint for sentiment-related routes
sentiment_bp = Blueprint(
    'sentiment', 
    __name__,
    template_folder='templates', # Specifies where Flask should look for templates
    static_folder='static'       # Specifies where Flask should look for static files
)

# Get the logger instance
logger = configure_logger() 

@sentiment_bp.route('/', methods=['GET'])
def index():
    """
    Renders the main index page.
    """
    # This route will serve the initial HTML form.
    return render_template('index.html')

@sentiment_bp.route('/analyze', methods=['POST', 'GET'])
# Cache the response for 3600 seconds (1 hour).
# The cache key is generated from the 'topic' form field or query argument.
@cache.cached(timeout=3600, key_prefix=lambda: request.form.get('topic') or request.args.get('topic', ''))
def analyze_sentiment_route():
    """
    Analyzes sentiment for a given topic from Reddit and displays results.
    Fetches data from cache/database first, then from Reddit if not found.
    """
    # Get 'topic' from form data (POST) or query arguments (GET)
    topic = request.form.get('topic') or request.args.get('topic')
    # Get 'num_records' (limit) from form data or query arguments, default to 10
    limit = int(request.form.get('num_records', request.args.get('num_records', 10))) 

    # Validate if topic is provided
    if not topic:
        # Return a JSON error response if topic is missing
        return jsonify({"error": "Topic is required"}), 400

    sentiment_results = []
    # --- Check if data exists in database (using SQLAlchemy query) ---
    # Query for existing sentiment analysis records for the given topic,
    # ordered by creation time (descending), limited by 'limit'.
    db_records = SentimentAnalysis.query.filter_by(topic=topic).order_by(SentimentAnalysis.created_at.desc()).limit(limit).all()

    if db_records:
        logger.info(f"Data for topic '{topic}' fetched from database.")
        # Convert SQLAlchemy model objects to dictionaries for consistent processing
        sentiment_results = [
            {
                "title": record.title,
                "content": record.content,
                "sentiment": record.sentiment,
                "score": record.score
            }
            for record in db_records
        ]
    else:
        logger.info(f"No data for topic '{topic}' found in database. Fetching from Reddit.")
        # --- Fetch Reddit data if not in database ---
        posts = fetch_reddit_data(topic, limit)

        if not posts:
            logger.warning(f"No Reddit posts found for topic '{topic}'.")
            return jsonify({"message": f"No posts found for topic '{topic}' to analyze."}), 200

        # --- Analyze sentiment of fetched posts ---
        sentiment_results = analyze_sentiment(posts)

        # --- Save new results to database ---
        try:
            for result in sentiment_results:
                # Create a new SentimentAnalysis record and add to session
                new_record = SentimentAnalysis(
                    topic=topic,
                    title=result['title'],
                    content=result['content'],
                    sentiment=result['sentiment'],
                    score=result['score']
                )
                db.session.add(new_record)
            db.session.commit() # Commit all new records to the database
            logger.info(f"Sentiment analysis results for topic '{topic}' saved to database.")
        except Exception as e:
            db.session.rollback() # Rollback transaction in case of error
            logger.error(f"Error saving sentiment results to database: {e}")
            # Optionally, return an error response
            return jsonify({"error": "Failed to save results to database."}), 500

    # --- Generate graphs (bar chart and word cloud) ---
    # These functions return base64 encoded image strings
    bar_chart_b64, word_cloud_b64 = generate_graphs(sentiment_results, topic)

    # Render the template with the data and base64 images
    return render_template(
        'index.html',
        topic=topic,
        sentiment_results=sentiment_results,
        bar_chart_b64=bar_chart_b64,
        word_cloud_b64=word_cloud_b64
    )