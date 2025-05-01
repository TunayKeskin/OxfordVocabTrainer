#!/usr/bin/env python3
"""
Update the database with words extracted from Oxford PDFs.
"""

import json
import os
import sys
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import after sys.path update
from app import app, db
from models import Word

def update_database_with_extracted_words():
    """Update the database with words extracted from Oxford PDFs."""
    # Dictionary to track words we're adding to avoid duplicates
    processed_words = {}
    
    # Track statistics
    stats = {
        'total_added': 0,
        'oxford3000_added': 0,
        'oxford5000_added': 0,
        'skipped_duplicates': 0,
        'errors': 0
    }
    
    print("Starting database update with extracted words...")
    
    # Load Oxford 3000 words
    try:
        with open('static/data/oxford3000_extracted.json', 'r', encoding='utf-8') as f:
            oxford3000_words = json.load(f)
            
        print(f"Loaded {len(oxford3000_words)} words from Oxford 3000 extracted JSON")
        
        # Add each word to the database
        for i, word_data in enumerate(oxford3000_words):
            try:
                english = word_data.get('english', '').lower().strip()
                turkish = word_data.get('turkish', f"{english} (tr)")
                
                if not english:
                    stats['errors'] += 1
                    continue
                    
                # Skip if we've already processed this word
                if english in processed_words:
                    stats['skipped_duplicates'] += 1
                    continue
                    
                # Check if the word already exists in the database
                existing_word = Word.query.filter_by(english=english).first()
                
                if existing_word:
                    # Update existing word if needed
                    if existing_word.turkish != turkish or existing_word.word_list != 'oxford3000':
                        existing_word.turkish = turkish
                        existing_word.word_list = 'oxford3000'
                        stats['total_added'] += 1
                        stats['oxford3000_added'] += 1
                else:
                    # Add new word
                    new_word = Word(
                        english=english, 
                        turkish=turkish, 
                        word_list='oxford3000'
                    )
                    db.session.add(new_word)
                    stats['total_added'] += 1
                    stats['oxford3000_added'] += 1
                    
                # Mark as processed
                processed_words[english] = True
                
                # Commit changes every 100 words to avoid timeout
                if i > 0 and i % 100 == 0:
                    db.session.commit()
                    print(f"Saved {i} words so far...")
                
            except Exception as e:
                print(f"Error processing Oxford 3000 word '{english}': {e}")
                stats['errors'] += 1
            
        # Commit final changes for Oxford 3000 words
        db.session.commit()
        print(f"Successfully processed Oxford 3000 words. Added/updated {stats['oxford3000_added']} words.")
            
    except FileNotFoundError:
        print("Oxford 3000 extracted JSON file not found. Skipping...")
    except Exception as e:
        print(f"Error processing Oxford 3000 words: {e}")
        db.session.rollback()
    
    # Load Oxford 5000 words
    try:
        with open('static/data/oxford5000_extracted.json', 'r', encoding='utf-8') as f:
            oxford5000_words = json.load(f)
            
        print(f"Loaded {len(oxford5000_words)} words from Oxford 5000 extracted JSON")
        
        # Add each word to the database
        for i, word_data in enumerate(oxford5000_words):
            try:
                english = word_data.get('english', '').lower().strip()
                turkish = word_data.get('turkish', f"{english} (tr)")
                
                if not english:
                    stats['errors'] += 1
                    continue
                    
                # Skip if we've already processed this word
                if english in processed_words:
                    stats['skipped_duplicates'] += 1
                    continue
                    
                # Check if the word already exists in the database
                existing_word = Word.query.filter_by(english=english).first()
                
                if existing_word:
                    # Update existing word if needed
                    if existing_word.turkish != turkish or existing_word.word_list != 'oxford5000':
                        existing_word.turkish = turkish
                        existing_word.word_list = 'oxford5000'
                        stats['total_added'] += 1
                        stats['oxford5000_added'] += 1
                else:
                    # Add new word
                    new_word = Word(
                        english=english, 
                        turkish=turkish, 
                        word_list='oxford5000'
                    )
                    db.session.add(new_word)
                    stats['total_added'] += 1
                    stats['oxford5000_added'] += 1
                    
                # Mark as processed
                processed_words[english] = True
                
                # Commit changes every 100 words to avoid timeout
                if i > 0 and i % 100 == 0:
                    db.session.commit()
                    print(f"Saved {i} words so far...")
                
            except Exception as e:
                print(f"Error processing Oxford 5000 word '{english}': {e}")
                stats['errors'] += 1
            
        # Commit final changes for Oxford 5000 words
        db.session.commit()
        print(f"Successfully processed Oxford 5000 words. Added/updated {stats['oxford5000_added']} words.")
            
    except FileNotFoundError:
        print("Oxford 5000 extracted JSON file not found. Skipping...")
    except Exception as e:
        print(f"Error processing Oxford 5000 words: {e}")
        db.session.rollback()
    
    # Print final statistics
    print("\nDatabase Update Summary:")
    print(f"Total words added/updated: {stats['total_added']}")
    print(f"Oxford 3000 words added: {stats['oxford3000_added']}")
    print(f"Oxford 5000 words added: {stats['oxford5000_added']}")
    print(f"Duplicate entries skipped: {stats['skipped_duplicates']}")
    print(f"Errors encountered: {stats['errors']}")
    
    # Check total words in database
    total_words = Word.query.count()
    print(f"\nTotal words in database: {total_words}")
    oxford3000_count = Word.query.filter_by(word_list='oxford3000').count()
    oxford5000_count = Word.query.filter_by(word_list='oxford5000').count()
    print(f"Oxford 3000 words in database: {oxford3000_count}")
    print(f"Oxford 5000 words in database: {oxford5000_count}")

if __name__ == "__main__":
    with app.app_context():
        start_time = time.time()
        update_database_with_extracted_words()
        end_time = time.time()
        print(f"\nDatabase update completed in {end_time - start_time:.2f} seconds.")