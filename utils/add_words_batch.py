#!/usr/bin/env python3
"""
Add words to the database in smaller batches to avoid timeouts.
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

BATCH_SIZE = 100  # Process 100 words at a time

def add_oxford3000_batch(start_index, end_index):
    """Add a batch of Oxford 3000 words to the database."""
    
    stats = {'added': 0, 'updated': 0, 'skipped': 0, 'errors': 0}
    
    try:
        # Load the extracted words
        with open('static/data/oxford3000_extracted.json', 'r', encoding='utf-8') as f:
            all_words = json.load(f)
            
        # Get the batch of words to process
        batch = all_words[start_index:end_index]
        
        print(f"Processing Oxford 3000 batch from index {start_index} to {end_index-1}...")
        
        # Process each word in the batch
        for word_data in batch:
            try:
                english = word_data.get('english', '').lower().strip()
                turkish = word_data.get('turkish', f"{english} (tr)")
                
                if not english:
                    stats['errors'] += 1
                    continue
                
                # Check if the word already exists
                existing_word = Word.query.filter_by(english=english).first()
                
                if existing_word:
                    # Update if necessary
                    if existing_word.word_list != 'oxford3000':
                        existing_word.word_list = 'oxford3000'
                        if existing_word.turkish == f"{english} (Turkish)":
                            existing_word.turkish = turkish
                        stats['updated'] += 1
                    else:
                        stats['skipped'] += 1
                else:
                    # Add new word
                    new_word = Word(
                        english=english,
                        turkish=turkish,
                        word_list='oxford3000'
                    )
                    db.session.add(new_word)
                    stats['added'] += 1
            except Exception as e:
                print(f"Error processing word '{english}': {e}")
                stats['errors'] += 1
        
        # Commit changes
        db.session.commit()
        
        print(f"Batch completed: Added {stats['added']} words, Updated {stats['updated']}, "
              f"Skipped {stats['skipped']}, Errors {stats['errors']}")
              
        return stats
    except Exception as e:
        print(f"Error processing batch: {e}")
        db.session.rollback()
        return stats

def add_oxford5000_batch(start_index, end_index):
    """Add a batch of Oxford 5000 words to the database."""
    
    stats = {'added': 0, 'updated': 0, 'skipped': 0, 'errors': 0}
    
    try:
        # Load the extracted words
        with open('static/data/oxford5000_extracted.json', 'r', encoding='utf-8') as f:
            all_words = json.load(f)
            
        # Get the batch of words to process
        batch = all_words[start_index:end_index]
        
        print(f"Processing Oxford 5000 batch from index {start_index} to {end_index-1}...")
        
        # Process each word in the batch
        for word_data in batch:
            try:
                english = word_data.get('english', '').lower().strip()
                turkish = word_data.get('turkish', f"{english} (tr)")
                
                if not english:
                    stats['errors'] += 1
                    continue
                
                # Check if the word already exists
                existing_word = Word.query.filter_by(english=english).first()
                
                if existing_word:
                    # Update if necessary
                    if existing_word.word_list != 'oxford5000':
                        existing_word.word_list = 'oxford5000'
                        if existing_word.turkish == f"{english} (Turkish)":
                            existing_word.turkish = turkish
                        stats['updated'] += 1
                    else:
                        stats['skipped'] += 1
                else:
                    # Add new word
                    new_word = Word(
                        english=english,
                        turkish=turkish,
                        word_list='oxford5000'
                    )
                    db.session.add(new_word)
                    stats['added'] += 1
            except Exception as e:
                print(f"Error processing word '{english}': {e}")
                stats['errors'] += 1
        
        # Commit changes
        db.session.commit()
        
        print(f"Batch completed: Added {stats['added']} words, Updated {stats['updated']}, "
              f"Skipped {stats['skipped']}, Errors {stats['errors']}")
              
        return stats
    except Exception as e:
        print(f"Error processing batch: {e}")
        db.session.rollback()
        return stats

def get_oxford3000_batch_count():
    """Get the total number of batches for Oxford 3000 words."""
    try:
        with open('static/data/oxford3000_extracted.json', 'r', encoding='utf-8') as f:
            all_words = json.load(f)
        
        total_words = len(all_words)
        batches = (total_words + BATCH_SIZE - 1) // BATCH_SIZE  # Ceiling division
        
        return total_words, batches
    except Exception as e:
        print(f"Error getting batch count: {e}")
        return 0, 0

def get_oxford5000_batch_count():
    """Get the total number of batches for Oxford 5000 words."""
    try:
        with open('static/data/oxford5000_extracted.json', 'r', encoding='utf-8') as f:
            all_words = json.load(f)
        
        total_words = len(all_words)
        batches = (total_words + BATCH_SIZE - 1) // BATCH_SIZE  # Ceiling division
        
        return total_words, batches
    except Exception as e:
        print(f"Error getting batch count: {e}")
        return 0, 0

def process_batch(list_type, batch_number):
    """Process a specific batch of words."""
    if list_type.lower() == 'oxford3000':
        total_words, total_batches = get_oxford3000_batch_count()
        
        if batch_number < 1 or batch_number > total_batches:
            print(f"Invalid batch number. Please enter a number between 1 and {total_batches}.")
            return
            
        start_index = (batch_number - 1) * BATCH_SIZE
        end_index = min(start_index + BATCH_SIZE, total_words)
        
        print(f"Processing Oxford 3000 batch {batch_number} of {total_batches}...")
        add_oxford3000_batch(start_index, end_index)
        
    elif list_type.lower() == 'oxford5000':
        total_words, total_batches = get_oxford5000_batch_count()
        
        if batch_number < 1 or batch_number > total_batches:
            print(f"Invalid batch number. Please enter a number between 1 and {total_batches}.")
            return
            
        start_index = (batch_number - 1) * BATCH_SIZE
        end_index = min(start_index + BATCH_SIZE, total_words)
        
        print(f"Processing Oxford 5000 batch {batch_number} of {total_batches}...")
        add_oxford5000_batch(start_index, end_index)
        
    else:
        print("Invalid list type. Please use 'oxford3000' or 'oxford5000'.")

def print_batch_info():
    """Print information about available batches."""
    oxford3000_total, oxford3000_batches = get_oxford3000_batch_count()
    oxford5000_total, oxford5000_batches = get_oxford5000_batch_count()
    
    print("\nBatch Information:")
    print(f"Oxford 3000: {oxford3000_total} words, {oxford3000_batches} batches")
    print(f"Oxford 5000: {oxford5000_total} words, {oxford5000_batches} batches")
    print(f"Batch size: {BATCH_SIZE} words")
    
    # Print current database status
    total_words = Word.query.count()
    oxford3000_count = Word.query.filter_by(word_list='oxford3000').count()
    oxford5000_count = Word.query.filter_by(word_list='oxford5000').count()
    
    print("\nCurrent Database Status:")
    print(f"Total words: {total_words}")
    print(f"Oxford 3000 words: {oxford3000_count}")
    print(f"Oxford 5000 words: {oxford5000_count}")
    
    print("\nTo process a batch, run:")
    print("python utils/add_words_batch.py oxford3000 [batch_number]")
    print("python utils/add_words_batch.py oxford5000 [batch_number]")

def main():
    """Main function."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print_batch_info()
        return
        
    # Process the specified batch
    if len(sys.argv) >= 3:
        list_type = sys.argv[1]
        try:
            batch_number = int(sys.argv[2])
            process_batch(list_type, batch_number)
        except ValueError:
            print("Invalid batch number. Please enter a number.")
            return
    else:
        print_batch_info()

if __name__ == "__main__":
    with app.app_context():
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"\nExecution completed in {end_time - start_time:.2f} seconds.")