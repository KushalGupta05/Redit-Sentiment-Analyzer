import os
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine # Import create_engine
from sqlalchemy.orm import sessionmaker # Import sessionmaker

# Initialize SQLAlchemy database object
db = SQLAlchemy()
# Initialize Flask-Caching object
cache = Cache()

def create_app():
    # Create Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Enable Cross-Origin Resource Sharing (CORS) for the app
    CORS(app)

    # --- SQLAlchemy Configuration ---
    # Get database URI from environment variables.
    # Default to a local SQLite database if not set.
    database_url = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///sentiments.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # Disable SQLAlchemy event system to save memory
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the Flask app
    db.init_app(app)

    # --- Flask-Caching Configuration ---
    # Get cache type from environment variables, default to 'simple' (in-memory)
    app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'simple')
    # Redis URL (if CACHE_TYPE is 'redis')
    app.config['CACHE_REDIS_URL'] = os.getenv('CACHE_REDIS_URL')
    # Redis port (might be redundant if URL includes it, but kept for consistency)
    app.config['CACHE_REDIS_PORT'] = os.getenv('CACHE_REDIS_PORT')
    # Default cache timeout in seconds, default to 3600 (1 hour)
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 3600))
    
    # Initialize the cache with the Flask app
    cache.init_app(app)

    # Import and register the sentiment blueprint
    from app.routes import sentiment_bp
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')

    return app