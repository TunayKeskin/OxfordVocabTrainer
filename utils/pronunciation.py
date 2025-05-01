import os
import logging
from gtts import gTTS
from pathlib import Path

def generate_pronunciation(word):
    """
    Generate pronunciation audio for a word using Google Text-to-Speech
    
    Args:
        word (str): The word to generate pronunciation for
        
    Returns:
        str: The path to the audio file, or None if generation failed
    """
    try:
        # Create pronunciation directory if it doesn't exist
        pron_dir = Path("static/audio/pronunciations")
        pron_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a sanitized filename
        filename = f"{word.lower().replace(' ', '_')}.mp3"
        file_path = pron_dir / filename
        
        # Check if file already exists
        if file_path.exists():
            return str(file_path)
        
        # Generate pronunciation
        tts = gTTS(text=word, lang='en', slow=False)
        tts.save(str(file_path))
        
        logging.debug(f"Generated pronunciation for '{word}' at {file_path}")
        
        return str(file_path)
    except Exception as e:
        logging.error(f"Error generating pronunciation for '{word}': {e}")
        return None