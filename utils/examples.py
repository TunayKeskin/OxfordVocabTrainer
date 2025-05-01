import logging
import requests
import os

def generate_examples_for_word(word, max_examples=3):
    """
    Generate example sentences for a given word
    
    Args:
        word (str): The word to generate examples for
        max_examples (int): Maximum number of examples to return
        
    Returns:
        list: A list of dictionaries with example sentences
    """
    try:
        logging.debug(f"Generating examples for word: {word}")
        
        # Initialize examples list
        examples = []
        
        # This is a simple implementation to generate examples
        # In a production environment, you would use a proper API
        # like Oxford Dictionary API, WordsAPI, etc.
        
        # For now, we'll use a simple free API that doesn't require authentication
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=5
        )
        
        if response.status_code != 200:
            logging.warning(f"Failed to get examples for {word}. Status code: {response.status_code}")
            return examples
        
        data = response.json()
        
        # Extract examples from the API response
        for entry in data:
            for meaning in entry.get('meanings', []):
                for definition in meaning.get('definitions', []):
                    example = definition.get('example')
                    if example and len(examples) < max_examples:
                        # Create a dictionary with English example
                        # For Turkish translation, in a real app you would use a translation API
                        examples.append({
                            "english_sentence": example,
                            "turkish_sentence": f"[Turkish translation would be here]"  # Placeholder
                        })
        
        logging.debug(f"Generated {len(examples)} examples for word: {word}")
        return examples[:max_examples]
        
    except Exception as e:
        logging.error(f"Error generating examples: {e}")
        return []
