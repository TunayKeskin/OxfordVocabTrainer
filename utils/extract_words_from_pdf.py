#!/usr/bin/env python3
"""
Extract words from Oxford 3000 and 5000 PDF files.
This script uses pdfminer.six to extract text from PDFs and parse the Oxford word lists.
"""

import io
import json
import os
import re
import sys
from typing import Dict, List, Any

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Create a directory to store the processed word lists
os.makedirs('static/data', exist_ok=True)

# Text patterns to identify word entries in the Oxford word lists
OXFORD_3000_PATTERN = r'([a-zA-Z\-\'(),]+(?:\s[a-zA-Z\-\'(),]+)*)\s+(?:(?:n\.|v\.|adj\.|adv\.|conj\.|det\.|pron\.|prep\.|exclam\.|number|auxiliary v\.|modal v\.|suffix|prefix)(?:[,\s][a-z\.]+)*)\s+([A-C][1-2])'
OXFORD_5000_PATTERN = r'([a-zA-Z\-\'(),0-9]+(?:\s[a-zA-Z\-\'(),0-9]+)*)\s+(?:(?:n\.|v\.|adj\.|adv\.|conj\.|det\.|pron\.|prep\.|exclam\.|number|auxiliary v\.|modal v\.|suffix|prefix)(?:[,\s][a-z\.]+)*)\s+([B-C][1-2])'

# Default Turkish translations
DEFAULT_TURKISH_SUFFIX = "(tr)"

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    output_string = io.StringIO()
    
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    
    text = output_string.getvalue()
    output_string.close()
    
    return text

def clean_word(word: str) -> str:
    """Clean a word by removing special characters and trailing whitespace."""
    # Remove parentheses and content within them
    word = re.sub(r'\([^)]*\)', '', word)
    
    # Remove special characters
    word = re.sub(r'[^\w\s\-\']', '', word)
    
    # Remove extra whitespace
    word = re.sub(r'\s+', ' ', word).strip()
    
    return word.lower()

def extract_oxford_words(text: str, pattern: str, word_list_name: str) -> List[Dict[str, Any]]:
    """Extract Oxford words from the provided text."""
    words = []
    matches = re.findall(pattern, text)
    
    seen_words = set()
    
    for match in matches:
        if len(match) >= 2:
            word = match[0].strip()
            level = match[-1].strip()
            
            # Extract part of speech
            pos_match = re.search(r'(?:n\.|v\.|adj\.|adv\.|conj\.|det\.|pron\.|prep\.|exclam\.|number|auxiliary v\.|modal v\.|suffix|prefix)(?:[,\s][a-z\.]+)*', word)
            pos = ''
            if pos_match:
                pos = pos_match.group(0).strip()
                word = word.replace(pos, '').strip()
            
            # Clean the word
            word = clean_word(word)
            
            # Skip if empty or duplicated
            if not word or word in seen_words:
                continue
                
            # Create Turkish translation
            turkish = f"{word} {DEFAULT_TURKISH_SUFFIX}"
            
            words.append({
                "english": word,
                "turkish": turkish,
                "word_list": word_list_name,
                "pos": pos,
                "level": level
            })
            
            seen_words.add(word)
    
    return words

def save_words_to_json(words: List[Dict[str, Any]], filename: str) -> None:
    """Save the extracted words to a JSON file."""
    with open(f"static/data/{filename}", 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(words)} words to static/data/{filename}")

def process_oxford_pdf(pdf_path: str, pattern: str, word_list_name: str) -> List[Dict[str, Any]]:
    """Process an Oxford PDF file and extract words."""
    print(f"Processing {pdf_path}...")
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Extract words from text
        words = extract_oxford_words(text, pattern, word_list_name)
        
        print(f"Extracted {len(words)} words from {pdf_path}")
        
        return words
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return []

def main():
    """Main function to process Oxford PDFs."""
    # Check if PDF files exist
    oxford_3000_path = 'attached_assets/The_Oxford_3000.pdf'
    oxford_5000_path = 'attached_assets/American_Oxford_5000.pdf'
    
    if not os.path.exists(oxford_3000_path):
        print(f"Error: {oxford_3000_path} not found")
        return
        
    if not os.path.exists(oxford_5000_path):
        print(f"Error: {oxford_5000_path} not found")
        return
    
    # Process Oxford 3000 PDF
    oxford_3000_words = process_oxford_pdf(
        oxford_3000_path, 
        OXFORD_3000_PATTERN, 
        'oxford3000'
    )
    
    # Process Oxford 5000 PDF
    oxford_5000_words = process_oxford_pdf(
        oxford_5000_path, 
        OXFORD_5000_PATTERN, 
        'oxford5000'
    )
    
    # Save to JSON files
    save_words_to_json(oxford_3000_words, "oxford3000_extracted.json")
    save_words_to_json(oxford_5000_words, "oxford5000_extracted.json")
    
    # Combine words
    combined_words = oxford_3000_words + oxford_5000_words
    
    # Remove duplicates
    seen_words = set()
    unique_words = []
    
    for word in combined_words:
        if word['english'] not in seen_words:
            unique_words.append(word)
            seen_words.add(word['english'])
    
    # Save combined list
    save_words_to_json(unique_words, "combined_extracted.json")
    
    print("\nExtraction completed!")
    print(f"Oxford 3000 words: {len(oxford_3000_words)}")
    print(f"Oxford 5000 words: {len(oxford_5000_words)}")
    print(f"Total unique words: {len(unique_words)}")
    
    # Print sample words
    if oxford_3000_words:
        print("\nSample words from Oxford 3000:")
        for word in oxford_3000_words[:5]:
            print(f"{word['english']} - Level: {word['level']}")
    
    if oxford_5000_words:
        print("\nSample words from Oxford 5000:")
        for word in oxford_5000_words[:5]:
            print(f"{word['english']} - Level: {word['level']}")

if __name__ == "__main__":
    main()