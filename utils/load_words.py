import json
import os
import sys

# Add the root directory to the Python path so we can import from app and models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Word

def load_words_from_json():
    """Load words from JSON files into the database"""
    with app.app_context():
        # Check if there are already words in the database
        existing_words = Word.query.count()
        if existing_words > 0:
            print(f"Database already contains {existing_words} words. Skipping import.")
            return
        
        # Load Oxford 3000 words
        try:
            with open("static/data/oxford3000.json", "r", encoding="utf-8") as f:
                oxford3000 = json.load(f)
                
            # Load Oxford 5000 words
            with open("static/data/oxford5000.json", "r", encoding="utf-8") as f:
                oxford5000 = json.load(f)
            
            # Create words in the database
            for word_data in oxford3000:
                word = Word(
                    english=word_data["english"],
                    turkish=word_data["turkish"],
                    word_list="oxford3000"
                )
                db.session.add(word)
            
            for word_data in oxford5000:
                word = Word(
                    english=word_data["english"],
                    turkish=word_data["turkish"],
                    word_list="oxford5000"
                )
                db.session.add(word)
            
            # Commit the changes
            db.session.commit()
            print(f"Successfully imported {len(oxford3000)} Oxford 3000 words and {len(oxford5000)} Oxford 5000 words.")
        except Exception as e:
            print(f"Error importing words: {e}")
            db.session.rollback()

if __name__ == "__main__":
    load_words_from_json()