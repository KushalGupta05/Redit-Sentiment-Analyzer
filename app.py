import os
from dotenv import load_dotenv
from app import create_app, db
import nltk

# Load environment variables from .env file
load_dotenv()

# --- NLTK Data Path Configuration ---
# Ensure NLTK can find its data by adding a custom path.
# This path should point to where 'vader_lexicon' and 'stopwords' will be downloaded.
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
# Add the custom NLTK data path if it's not already in the list
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)
    print(f"Added NLTK data path: {nltk_data_path}")

# --- NLTK Data Download ---
# Directly attempt to download resources. NLTK's download function
# is designed to handle checking if resources exist and downloading if not.
# It will print its own messages for success or failure to the console.
print("Attempting to download NLTK 'vader_lexicon'...")
nltk.download('vader_lexicon', download_dir=nltk_data_path, quiet=False)

print("Attempting to download NLTK 'stopwords'...")
nltk.download('stopwords', download_dir=nltk_data_path, quiet=False)

# --- End NLTK Data Download ---


app = create_app()

with app.app_context():
    # Create database tables if they don't exist
    db.create_all()

if __name__ == '__main__':
    # Get the port from environment variables or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask application
    app.run(host='0.0.0.0', port=port, debug=True)
