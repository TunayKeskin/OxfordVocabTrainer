import logging

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
        return _generate_generic_examples(word, max_examples)
    except Exception as e:
        logging.error(f"Error generating examples for '{word}': {e}")
        return []

def _generate_generic_examples(word, count=3):
    """
    Generate generic example sentences
    
    Args:
        word (str): The word to generate examples for
        count (int): Number of examples to generate
        
    Returns:
        list: A list of dictionaries with example sentences
    """
    templates = [
        f"The word '{word}' is commonly used in everyday conversation.",
        f"Students often learn '{word}' as part of their vocabulary lessons.",
        f"When learning English, '{word}' is an important word to know.",
        f"You can improve your vocabulary by using '{word}' in a sentence.",
        f"'{word.capitalize()}' appears frequently in both written and spoken English."
    ]
    
    examples = []
    for i in range(min(count, len(templates))):
        examples.append({
            "english_sentence": templates[i],
            "turkish_sentence": f"Bu cümle '{word}' kelimesiyle ilgili bir örnektir."  # Generic Turkish placeholder
        })
    
    return examples