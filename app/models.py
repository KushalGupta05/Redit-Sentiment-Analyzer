from app import db
from datetime import datetime

# Define the SentimentAnalysis database model
class SentimentAnalysis(db.Model):
    # Set the table name in the database
    __tablename__ = 'sentiment_analysis'
    
    # Define columns
    id = db.Column(db.Integer, primary_key=True) 
    topic = db.Column(db.String(255), nullable=False) 
    title = db.Column(db.Text, nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    sentiment = db.Column(db.String(10), nullable=False) 
    score = db.Column(db.Float, nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # String representation of the object for debugging
    def __repr__(self):
        return f'<SentimentAnalysis {self.title}>'
