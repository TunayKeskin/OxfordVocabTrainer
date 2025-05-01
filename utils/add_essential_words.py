#!/usr/bin/env python3
"""
Add essential vocabulary words from the Oxford wordlists to the database.
This script focuses on adding a manageable set of important words.
"""

import json
import os
import sys
import time
from collections import defaultdict

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import after sys.path update
from app import app, db
from models import Word

def load_essential_words():
    """
    Load a selection of essential words from the extracted Oxford wordlists.
    Prioritizes words based on level and selects a balanced set from each letter.
    """
    # Dictionary to store words by first letter
    words_by_letter = defaultdict(list)
    all_words = []
    
    # Load Oxford 3000 words (higher priority)
    try:
        with open('static/data/oxford3000_extracted.json', 'r', encoding='utf-8') as f:
            oxford3000_words = json.load(f)
            
        print(f"Loaded {len(oxford3000_words)} words from Oxford 3000 extracted JSON")
        
        # Group words by first letter
        for word_data in oxford3000_words:
            english = word_data.get('english', '').lower().strip()
            if english:
                first_letter = english[0]
                if first_letter.isalpha():
                    words_by_letter[first_letter].append({
                        'english': english,
                        'turkish': word_data.get('turkish', f"{english} (tr)"),
                        'word_list': 'oxford3000',
                        'level': word_data.get('level', '')
                    })
    except Exception as e:
        print(f"Error loading Oxford 3000 words: {e}")
    
    # Load Oxford 5000 words
    try:
        with open('static/data/oxford5000_extracted.json', 'r', encoding='utf-8') as f:
            oxford5000_words = json.load(f)
            
        print(f"Loaded {len(oxford5000_words)} words from Oxford 5000 extracted JSON")
        
        # Group words by first letter
        for word_data in oxford5000_words:
            english = word_data.get('english', '').lower().strip()
            if english:
                first_letter = english[0]
                if first_letter.isalpha():
                    words_by_letter[first_letter].append({
                        'english': english,
                        'turkish': word_data.get('turkish', f"{english} (tr)"),
                        'word_list': 'oxford5000',
                        'level': word_data.get('level', '')
                    })
    except Exception as e:
        print(f"Error loading Oxford 5000 words: {e}")
    
    # Select a balanced set of words from each letter
    # For smaller letters (like X, Z), take more words to ensure coverage
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        letter_words = words_by_letter[letter]
        
        # Sort words by level (A1, A2, B1, B2, C1, C2)
        letter_words.sort(key=lambda w: (
            '0' if w['level'].startswith('A') else 
            '1' if w['level'].startswith('B') else 
            '2'
        ) + w['level'])
        
        # Determine how many words to take based on availability
        total_available = len(letter_words)
        
        # Take more words from less common letters
        if letter in 'jkqxz':
            words_to_take = min(total_available, 40)  # Take up to 40 words
        elif letter in 'vwy':
            words_to_take = min(total_available, 30)  # Take up to 30 words
        else:
            words_to_take = min(total_available, 25)  # Take up to 25 words for common letters
        
        # Add the selected words
        all_words.extend(letter_words[:words_to_take])
        
        print(f"Selected {words_to_take} words starting with '{letter}' (out of {total_available} available)")
    
    print(f"Total essential words selected: {len(all_words)}")
    return all_words

def add_words_to_database(words):
    """Add the selected words to the database."""
    
    stats = {
        'total': len(words),
        'added': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }
    
    print(f"Adding {len(words)} essential words to the database...")
    
    # Set to track words already processed in this batch
    processed_words = set()
    
    # Add words to the database
    for i, word_data in enumerate(words):
        try:
            english = word_data['english'].lower().strip()
            turkish = word_data['turkish']
            word_list = word_data['word_list']
            
            # Skip empty words
            if not english:
                stats['errors'] += 1
                continue
                
            # Skip if we've already processed this word in this batch
            if english in processed_words:
                stats['skipped'] += 1
                continue
            
            # Mark as processed
            processed_words.add(english)
            
            # Check if the word already exists
            existing_word = Word.query.filter_by(english=english).first()
            
            if existing_word:
                # Update if needed
                updated = False
                
                if existing_word.word_list != word_list:
                    existing_word.word_list = word_list
                    updated = True
                    
                if existing_word.turkish == f"{english} (Turkish)" and turkish != existing_word.turkish:
                    existing_word.turkish = turkish
                    updated = True
                
                if updated:
                    stats['updated'] += 1
                else:
                    stats['skipped'] += 1
            else:
                # Add new word
                new_word = Word(
                    english=english,
                    turkish=turkish,
                    word_list=word_list
                )
                db.session.add(new_word)
                stats['added'] += 1
            
            # Commit changes every 50 words to avoid timeout
            if (i + 1) % 50 == 0:
                db.session.commit()
                print(f"Processed {i + 1}/{len(words)} words...")
                
        except Exception as e:
            print(f"Error processing word '{english}': {e}")
            stats['errors'] += 1
    
    # Commit final changes
    db.session.commit()
    
    print(f"\nDatabase Update Summary:")
    print(f"Total words processed: {stats['total']}")
    print(f"New words added: {stats['added']}")
    print(f"Existing words updated: {stats['updated']}")
    print(f"Words skipped (already exist): {stats['skipped']}")
    print(f"Errors encountered: {stats['errors']}")
    
    # Check total words in database
    total_words = Word.query.count()
    oxford3000_count = Word.query.filter_by(word_list='oxford3000').count()
    oxford5000_count = Word.query.filter_by(word_list='oxford5000').count()
    
    print(f"\nDatabase Status After Update:")
    print(f"Total words in database: {total_words}")
    print(f"Oxford 3000 words: {oxford3000_count}")
    print(f"Oxford 5000 words: {oxford5000_count}")

def main():
    """Main function to add essential words to the database."""
    # Load essential words
    essential_words = load_essential_words()
    
    # Add words to the database
    add_words_to_database(essential_words)

if __name__ == "__main__":
    with app.app_context():
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"\nExecution completed in {end_time - start_time:.2f} seconds.")