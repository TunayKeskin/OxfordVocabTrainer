#!/usr/bin/env python3
"""
Add words to ensure coverage across the entire alphabet.
This script adds a smaller set of words (5-10 per letter) to ensure good alphabet coverage.
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import after sys.path update
from app import app, db
from models import Word

# Words covering the entire alphabet (A-Z)
# These are common Oxford words with their Turkish translations
ALPHABET_WORDS = [
    # A
    {"english": "abandon", "turkish": "terk etmek", "word_list": "oxford3000"},
    {"english": "ability", "turkish": "yetenek", "word_list": "oxford3000"},
    {"english": "about", "turkish": "hakkında", "word_list": "oxford3000"},
    {"english": "above", "turkish": "yukarıda", "word_list": "oxford3000"},
    {"english": "abroad", "turkish": "yurtdışında", "word_list": "oxford3000"},
    
    # B
    {"english": "baby", "turkish": "bebek", "word_list": "oxford3000"},
    {"english": "back", "turkish": "geri", "word_list": "oxford3000"},
    {"english": "bad", "turkish": "kötü", "word_list": "oxford3000"},
    {"english": "bag", "turkish": "çanta", "word_list": "oxford3000"},
    {"english": "balance", "turkish": "denge", "word_list": "oxford3000"},
    
    # C
    {"english": "cake", "turkish": "pasta", "word_list": "oxford3000"},
    {"english": "call", "turkish": "aramak", "word_list": "oxford3000"},
    {"english": "camera", "turkish": "kamera", "word_list": "oxford3000"},
    {"english": "car", "turkish": "araba", "word_list": "oxford3000"},
    {"english": "cat", "turkish": "kedi", "word_list": "oxford3000"},
    
    # D
    {"english": "dad", "turkish": "baba", "word_list": "oxford3000"},
    {"english": "daily", "turkish": "günlük", "word_list": "oxford3000"},
    {"english": "damage", "turkish": "hasar", "word_list": "oxford3000"},
    {"english": "dance", "turkish": "dans", "word_list": "oxford3000"},
    {"english": "dark", "turkish": "karanlık", "word_list": "oxford3000"},
    
    # E
    {"english": "each", "turkish": "her biri", "word_list": "oxford3000"},
    {"english": "ear", "turkish": "kulak", "word_list": "oxford3000"},
    {"english": "early", "turkish": "erken", "word_list": "oxford3000"},
    {"english": "earth", "turkish": "dünya", "word_list": "oxford3000"},
    {"english": "east", "turkish": "doğu", "word_list": "oxford3000"},
    
    # F
    {"english": "face", "turkish": "yüz", "word_list": "oxford3000"},
    {"english": "fact", "turkish": "gerçek", "word_list": "oxford3000"},
    {"english": "fail", "turkish": "başarısız olmak", "word_list": "oxford3000"},
    {"english": "fair", "turkish": "adil", "word_list": "oxford3000"},
    {"english": "fall", "turkish": "düşmek", "word_list": "oxford3000"},
    
    # G
    {"english": "game", "turkish": "oyun", "word_list": "oxford3000"},
    {"english": "garden", "turkish": "bahçe", "word_list": "oxford3000"},
    {"english": "gas", "turkish": "gaz", "word_list": "oxford3000"},
    {"english": "girl", "turkish": "kız", "word_list": "oxford3000"},
    {"english": "give", "turkish": "vermek", "word_list": "oxford3000"},
    
    # H
    {"english": "habit", "turkish": "alışkanlık", "word_list": "oxford3000"},
    {"english": "hair", "turkish": "saç", "word_list": "oxford3000"},
    {"english": "half", "turkish": "yarım", "word_list": "oxford3000"},
    {"english": "hand", "turkish": "el", "word_list": "oxford3000"},
    {"english": "happy", "turkish": "mutlu", "word_list": "oxford3000"},
    
    # I
    {"english": "ice", "turkish": "buz", "word_list": "oxford3000"},
    {"english": "idea", "turkish": "fikir", "word_list": "oxford3000"},
    {"english": "if", "turkish": "eğer", "word_list": "oxford3000"},
    {"english": "ill", "turkish": "hasta", "word_list": "oxford3000"},
    {"english": "image", "turkish": "görüntü", "word_list": "oxford3000"},
    
    # J
    {"english": "jacket", "turkish": "ceket", "word_list": "oxford3000"},
    {"english": "job", "turkish": "iş", "word_list": "oxford3000"},
    {"english": "join", "turkish": "katılmak", "word_list": "oxford3000"},
    {"english": "joke", "turkish": "şaka", "word_list": "oxford3000"},
    {"english": "journey", "turkish": "yolculuk", "word_list": "oxford3000"},
    
    # K
    {"english": "keep", "turkish": "tutmak", "word_list": "oxford3000"},
    {"english": "key", "turkish": "anahtar", "word_list": "oxford3000"},
    {"english": "kick", "turkish": "tekmelemek", "word_list": "oxford3000"},
    {"english": "kid", "turkish": "çocuk", "word_list": "oxford3000"},
    {"english": "kill", "turkish": "öldürmek", "word_list": "oxford3000"},
    
    # L
    {"english": "lab", "turkish": "laboratuvar", "word_list": "oxford3000"},
    {"english": "lady", "turkish": "hanımefendi", "word_list": "oxford3000"},
    {"english": "lake", "turkish": "göl", "word_list": "oxford3000"},
    {"english": "land", "turkish": "arazi", "word_list": "oxford3000"},
    {"english": "language", "turkish": "dil", "word_list": "oxford3000"},
    
    # M
    {"english": "machine", "turkish": "makine", "word_list": "oxford3000"},
    {"english": "mad", "turkish": "çılgın", "word_list": "oxford3000"},
    {"english": "mail", "turkish": "posta", "word_list": "oxford3000"},
    {"english": "main", "turkish": "ana", "word_list": "oxford3000"},
    {"english": "make", "turkish": "yapmak", "word_list": "oxford3000"},
    
    # N
    {"english": "name", "turkish": "isim", "word_list": "oxford3000"},
    {"english": "nation", "turkish": "ulus", "word_list": "oxford3000"},
    {"english": "nature", "turkish": "doğa", "word_list": "oxford3000"},
    {"english": "near", "turkish": "yakın", "word_list": "oxford3000"},
    {"english": "need", "turkish": "ihtiyaç", "word_list": "oxford3000"},
    
    # O
    {"english": "object", "turkish": "nesne", "word_list": "oxford3000"},
    {"english": "occur", "turkish": "meydana gelmek", "word_list": "oxford3000"},
    {"english": "ocean", "turkish": "okyanus", "word_list": "oxford3000"},
    {"english": "offer", "turkish": "teklif etmek", "word_list": "oxford3000"},
    {"english": "office", "turkish": "ofis", "word_list": "oxford3000"},
    
    # P
    {"english": "page", "turkish": "sayfa", "word_list": "oxford3000"},
    {"english": "pain", "turkish": "acı", "word_list": "oxford3000"},
    {"english": "paper", "turkish": "kağıt", "word_list": "oxford3000"},
    {"english": "parent", "turkish": "ebeveyn", "word_list": "oxford3000"},
    {"english": "part", "turkish": "parça", "word_list": "oxford3000"},
    
    # Q
    {"english": "quality", "turkish": "kalite", "word_list": "oxford3000"},
    {"english": "question", "turkish": "soru", "word_list": "oxford3000"},
    {"english": "quick", "turkish": "hızlı", "word_list": "oxford3000"},
    {"english": "quiet", "turkish": "sessiz", "word_list": "oxford3000"},
    {"english": "quit", "turkish": "bırakmak", "word_list": "oxford3000"},
    
    # R
    {"english": "race", "turkish": "yarış", "word_list": "oxford3000"},
    {"english": "radio", "turkish": "radyo", "word_list": "oxford3000"},
    {"english": "rain", "turkish": "yağmur", "word_list": "oxford3000"},
    {"english": "read", "turkish": "okumak", "word_list": "oxford3000"},
    {"english": "real", "turkish": "gerçek", "word_list": "oxford3000"},
    
    # S
    {"english": "sad", "turkish": "üzgün", "word_list": "oxford3000"},
    {"english": "safe", "turkish": "güvenli", "word_list": "oxford3000"},
    {"english": "same", "turkish": "aynı", "word_list": "oxford3000"},
    {"english": "school", "turkish": "okul", "word_list": "oxford3000"},
    {"english": "sea", "turkish": "deniz", "word_list": "oxford3000"},
    
    # T
    {"english": "table", "turkish": "masa", "word_list": "oxford3000"},
    {"english": "take", "turkish": "almak", "word_list": "oxford3000"},
    {"english": "talk", "turkish": "konuşmak", "word_list": "oxford3000"},
    {"english": "tea", "turkish": "çay", "word_list": "oxford3000"},
    {"english": "team", "turkish": "takım", "word_list": "oxford3000"},
    
    # U
    {"english": "ugly", "turkish": "çirkin", "word_list": "oxford3000"},
    {"english": "uncle", "turkish": "amca", "word_list": "oxford3000"},
    {"english": "under", "turkish": "altında", "word_list": "oxford3000"},
    {"english": "understand", "turkish": "anlamak", "word_list": "oxford3000"},
    {"english": "university", "turkish": "üniversite", "word_list": "oxford3000"},
    
    # V
    {"english": "vacation", "turkish": "tatil", "word_list": "oxford3000"},
    {"english": "valley", "turkish": "vadi", "word_list": "oxford3000"},
    {"english": "value", "turkish": "değer", "word_list": "oxford3000"},
    {"english": "vegetable", "turkish": "sebze", "word_list": "oxford3000"},
    {"english": "video", "turkish": "video", "word_list": "oxford3000"},
    
    # W
    {"english": "wage", "turkish": "ücret", "word_list": "oxford3000"},
    {"english": "wait", "turkish": "beklemek", "word_list": "oxford3000"},
    {"english": "walk", "turkish": "yürümek", "word_list": "oxford3000"},
    {"english": "want", "turkish": "istemek", "word_list": "oxford3000"},
    {"english": "war", "turkish": "savaş", "word_list": "oxford3000"},
    
    # X
    {"english": "x-ray", "turkish": "röntgen", "word_list": "oxford5000"},
    {"english": "xenophobia", "turkish": "yabancı düşmanlığı", "word_list": "oxford5000"},
    
    # Y
    {"english": "yard", "turkish": "bahçe", "word_list": "oxford3000"},
    {"english": "year", "turkish": "yıl", "word_list": "oxford3000"},
    {"english": "yellow", "turkish": "sarı", "word_list": "oxford3000"},
    {"english": "yes", "turkish": "evet", "word_list": "oxford3000"},
    {"english": "yesterday", "turkish": "dün", "word_list": "oxford3000"},
    
    # Z
    {"english": "zero", "turkish": "sıfır", "word_list": "oxford3000"},
    {"english": "zone", "turkish": "bölge", "word_list": "oxford3000"},
    {"english": "zoom", "turkish": "yakınlaştırmak", "word_list": "oxford5000"}
]

def add_words_to_database():
    """Add words to the database."""
    total_words = len(ALPHABET_WORDS)
    print(f"Adding {total_words} words covering the entire alphabet...")
    
    stats = {
        'added': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }
    
    # Add words to the database
    for i, word_data in enumerate(ALPHABET_WORDS):
        try:
            english = word_data['english'].lower().strip()
            turkish = word_data['turkish']
            word_list = word_data['word_list']
            
            # Check if the word already exists
            existing_word = Word.query.filter_by(english=english).first()
            
            if existing_word:
                # Word already exists
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
                
            # Commit changes every 10 words
            if (i + 1) % 10 == 0:
                db.session.commit()
                print(f"Processed {i + 1}/{total_words} words...")
                
        except Exception as e:
            print(f"Error processing word '{english}': {e}")
            stats['errors'] += 1
    
    # Commit final changes
    db.session.commit()
    
    print(f"\nDatabase Update Summary:")
    print(f"New words added: {stats['added']}")
    print(f"Words already exist (skipped): {stats['skipped']}")
    print(f"Errors encountered: {stats['errors']}")
    
    # Count words in database by starting letter
    letters = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        count = Word.query.filter(Word.english.like(f'{letter}%')).count()
        letters[letter] = count
    
    print("\nWords in database by starting letter:")
    for letter, count in letters.items():
        print(f"{letter}: {count}")
    
    # Check total words in database
    total_words = Word.query.count()
    oxford3000_count = Word.query.filter_by(word_list='oxford3000').count()
    oxford5000_count = Word.query.filter_by(word_list='oxford5000').count()
    
    print(f"\nDatabase Status:")
    print(f"Total words in database: {total_words}")
    print(f"Oxford 3000 words: {oxford3000_count}")
    print(f"Oxford 5000 words: {oxford5000_count}")

def main():
    """Main function to add words to the database."""
    add_words_to_database()

if __name__ == "__main__":
    with app.app_context():
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"\nExecution completed in {end_time - start_time:.2f} seconds.")