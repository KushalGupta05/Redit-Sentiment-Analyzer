from app import db
from datetime import datetime

# Define the SentimentAnalysis database model
class SentimentAnalysis(db.Model):
    # Set the table name in the database
    __tablename__ = 'sentiment_analysis'
    
    # Define columns
    id = db.Column(db.Integer, primary_key=True) # Primary key, auto-increments
    topic = db.Column(db.String(255), nullable=False) # Topic of the analysis (e.g., "science", "technology")
    title = db.Column(db.Text, nullable=False) # Title of the Reddit post
    content = db.Column(db.Text, nullable=False) # Full content of the Reddit post
    sentiment = db.Column(db.String(10), nullable=False) # Sentiment label (e.g., "POSITIVE", "NEGATIVE", "NEUTRAL")
    score = db.Column(db.Float, nullable=False) # Compound sentiment score
    created_at = db.Column(db.DateTime, server_default=db.func.now()) # Timestamp of record creation, defaults to current time

    # String representation of the object for debugging
    def __repr__(self):
        return f'<SentimentAnalysis {self.title}>'
