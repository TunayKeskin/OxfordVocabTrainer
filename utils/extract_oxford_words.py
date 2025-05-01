#!/usr/bin/env python3
"""
This script extracts Oxford 3000 and Oxford 5000 words from the provided PDF text
and generates JSON files for use in the OxfordVocabQuiz application.

Note: Since we can't directly read the PDF files, this script works with the text
content that has been extracted from the PDFs.
"""

import json
import os
import re
from typing import List, Dict, Any

# Create a directory to store the processed word lists
os.makedirs('static/data', exist_ok=True)

# Text patterns to identify word entries in the Oxford word lists
OXFORD_3000_PATTERN = r"([a-zA-Z\-',]+(?:\s[a-zA-Z\-',]+)*)\s+((?:n\.|v\.|adj\.|adv\.|conj\.|det\.|pron\.|prep\.|exclam\.|number|auxiliary v\.|modal v\.|suffix|prefix)\.?(?:\s[a-z\.]+)*)\s+([A-C][1-2])(?:\s+|$)"
OXFORD_5000_PATTERN = r"([a-zA-Z\-',]+(?:\s[a-zA-Z\-',]+)*)\s+((?:n\.|v\.|adj\.|adv\.|conj\.|det\.|pron\.|prep\.|exclam\.|number|auxiliary v\.|modal v\.|suffix|prefix)\.?(?:\s[a-z\.]+)*)\s+([B-C][1-2])(?:\s+|$)"

# Turkish translations for Oxford 3000/5000 words
# This is a sample of common translations that will be expanded with more words
turkish_translations = {
    # A
    "abandon": "terk etmek",
    "ability": "yetenek",
    "able": "yapabilir",
    "about": "hakkında",
    "above": "yukarıda",
    "abroad": "yurtdışında",
    "absence": "yokluk",
    "absolute": "mutlak",
    "absolutely": "kesinlikle",
    "absorb": "emmek",
    "abstract": "soyut",
    "academic": "akademik",
    "accept": "kabul etmek",
    "access": "erişim",
    "accident": "kaza",
    "accompany": "eşlik etmek",
    "according to": "göre",
    "account": "hesap",
    "accurate": "doğru",
    "accusation": "suçlama",
    "accuse": "suçlamak",
    "achieve": "başarmak",
    "achievement": "başarı",
    "acknowledge": "kabul etmek",
    "acquire": "edinmek",
    "across": "karşısında",
    "act": "davranmak",
    "action": "eylem",
    "active": "aktif",
    "activity": "aktivite",
    "actor": "aktör",
    "actress": "aktris",
    "actual": "gerçek",
    "actually": "aslında",
    "adapt": "uyarlamak",
    "add": "eklemek",
    "addition": "ekleme",
    "additional": "ek",
    "address": "adres",
    "administration": "yönetim",
    "admit": "kabul etmek",
    "adopt": "benimsemek",
    "adult": "yetişkin",
    "advance": "ilerlemek",
    "advanced": "ileri",
    "advantage": "avantaj",
    "adventure": "macera",
    "advertise": "reklam vermek",
    "advertisement": "reklam",
    "advice": "tavsiye",
    "advise": "tavsiye etmek",
    "affair": "ilişki",
    "affect": "etkilemek",
    "afford": "karşılayabilmek",
    "afraid": "korkmak",
    "after": "sonra",
    "afternoon": "öğleden sonra",
    "afterwards": "sonradan",
    "again": "tekrar",
    "against": "karşı",
    "age": "yaş",
    "agency": "acenta",
    "agenda": "gündem",
    "agent": "ajan",
    "aggressive": "agresif",
    "ago": "önce",
    "agree": "katılmak",
    "agreement": "anlaşma",
    "ahead": "ileride",
    "aid": "yardım",
    "aim": "amaçlamak",
    "air": "hava",
    "aircraft": "uçak",
    "airline": "havayolu",
    "airport": "havaalanı",
    "alarm": "alarm",
    "album": "albüm",
    "alcohol": "alkol",
    "alive": "canlı",
    "all": "hepsi",
    "allow": "izin vermek",
    "almost": "neredeyse",
    "alone": "yalnız",
    "along": "boyunca",
    "already": "zaten",
    "also": "ayrıca",
    "alter": "değiştirmek",
    "alternative": "alternatif",
    "although": "rağmen",
    "always": "her zaman",
    "amazing": "şaşırtıcı",
    "ambition": "hırs",
    "ambitious": "hırslı",
    "among": "arasında",
    "amount": "miktar",
    "analyse": "analiz etmek",
    "analysis": "analiz",
    "ancient": "antik",
    "and": "ve",
    "anger": "öfke",
    "angle": "açı",
    "angry": "kızgın",
    "animal": "hayvan",
    "ankle": "ayak bileği",
    "anniversary": "yıldönümü",
    "announce": "duyurmak",
    "announcement": "duyuru",
    "annoy": "rahatsız etmek",
    "annual": "yıllık",
    "another": "başka bir",
    "answer": "cevaplamak",
    "anxious": "endişeli",
    "any": "herhangi bir",
    "anybody": "herkes",
    "anyone": "herhangi biri",
    "anything": "herhangi bir şey",
    "anyway": "her neyse",
    "anywhere": "herhangi bir yerde",
    "apart": "ayrı",
    "apartment": "daire",
    "apologize": "özür dilemek",
    "app": "uygulama",
    "apparent": "bariz",
    "apparently": "görünüşe göre",
    "appeal": "çekicilik",
    "appear": "görünmek",
    "appearance": "görünüş",
    "apple": "elma",
    "application": "uygulama",
    "apply": "uygulamak",
    "appointment": "randevu",
    "appreciate": "takdir etmek",
    "approach": "yaklaşmak",
    "appropriate": "uygun",
    "approval": "onay",
    "approve": "onaylamak",
    "approximately": "yaklaşık olarak",
    "architect": "mimar",
    "architecture": "mimari",
    "area": "alan",
    "argue": "tartışmak",
    "argument": "tartışma",
    "arise": "ortaya çıkmak",
    "arm": "kol",
    "armed": "silahlı",
    "army": "ordu",
    "around": "etrafında",
    "arrange": "düzenlemek",
    "arrangement": "düzenleme",
    "arrest": "tutuklamak",
    "arrival": "varış",
    "arrive": "varmak",
    "art": "sanat",
    "article": "makale",
    "artificial": "yapay",
    "artist": "sanatçı",
    "artistic": "sanatsal",
    "as": "olarak",
    "ashamed": "utanmış",
    "ask": "sormak",
    "asleep": "uykuda",
    "aspect": "yön",
    "assess": "değerlendirmek",
    "assessment": "değerlendirme",
    "assignment": "görev",
    "assist": "yardım etmek",
    "assistant": "asistan",
    "associate": "ilişkilendirmek",
    "association": "dernek",
    "assume": "varsaymak",
    "at": "de/da",
    "athlete": "atlet",
    "atmosphere": "atmosfer",
    "attach": "eklemek",
    "attack": "saldırmak",
    "attempt": "denemek",
    "attend": "katılmak",
    "attention": "dikkat",
    "attitude": "tutum",
    "attract": "çekmek",
    "attraction": "çekim",
    "attractive": "çekici",
    "audience": "seyirci",
    "author": "yazar",
    "authority": "yetki",
    "available": "mevcut",
    "average": "ortalama",
    "avoid": "kaçınmak",
    "award": "ödül",
    "aware": "farkında",
    "away": "uzakta",
    "awful": "korkunç",
    
    # B
    "baby": "bebek",
    "back": "geri",
    "background": "arka plan",
    "backwards": "geriye doğru",
    "bacteria": "bakteri",
    "bad": "kötü",
    "badly": "kötü bir şekilde",
    "bag": "çanta",
    "bake": "pişirmek",
    "balance": "denge",
    "ball": "top",
    "ban": "yasaklamak",
    "banana": "muz",
    "band": "grup",
    "bank": "banka",
    "bar": "bar",
    "barrier": "engel",
    "base": "temel",
    "baseball": "beyzbol",
    "based": "dayalı",
    "basic": "temel",
    "basically": "temel olarak",
    "basis": "temel",
    "basketball": "basketbol",
    "bath": "banyo",
    "bathroom": "banyo",
    "battery": "pil",
    "battle": "savaş",
    "be": "olmak",
    "beach": "plaj",
    "bean": "fasulye",
    "bear": "ayı",
    "beat": "yenmek",
    "beautiful": "güzel",
    "beauty": "güzellik",
    "because": "çünkü",
    "become": "olmak",
    "bed": "yatak",
    "bedroom": "yatak odası",
    "bee": "arı",
    "beef": "sığır eti",
    "beer": "bira",
    "before": "önce",
    "begin": "başlamak",
    "beginning": "başlangıç",
    "behave": "davranmak",
    "behaviour": "davranış",
    "behind": "arkasında",
    "being": "varlık",
    "belief": "inanç",
    "believe": "inanmak",
    "bell": "zil",
    "belong": "ait olmak",
    "below": "aşağıda",
    "belt": "kemer",
    "bend": "bükmek",
    "benefit": "fayda",
    "bent": "eğilmiş",
    "best": "en iyi",
    "bet": "bahis",
    "better": "daha iyi",
    "between": "arasında",
    "beyond": "ötesinde",
    "bicycle": "bisiklet",
    "big": "büyük",
    "bike": "bisiklet",
    "bill": "fatura",
    "billion": "milyar",
    "bin": "çöp kutusu",
    "biology": "biyoloji",
    "bird": "kuş",
    "birth": "doğum",
    "birthday": "doğum günü",
    "biscuit": "bisküvi",
    "bit": "parça",
    "bite": "ısırmak",
    "bitter": "acı",
    "black": "siyah",
    "blame": "suçlamak",
    "blank": "boş",
    "blind": "kör",
    "block": "blok",
    "blog": "blog",
    "blonde": "sarışın",
    "blood": "kan",
    "blow": "üflemek",
    "blue": "mavi",
    "board": "tahta",
    "boat": "tekne",
    
    # ... More words will be added here
}

def extract_oxford_3000_words(text: str) -> List[Dict[str, Any]]:
    """
    Extract Oxford 3000 words from the provided text.
    
    Args:
        text: The text extracted from The Oxford 3000 PDF
        
    Returns:
        A list of dictionaries containing word information
    """
    words = []
    matches = re.findall(OXFORD_3000_PATTERN, text)
    
    for match in matches:
        word = match[0].strip().lower()
        pos = match[1].strip()
        level = match[2].strip()
        
        # Get Turkish translation or use placeholder
        turkish = turkish_translations.get(word, f"{word} (Turkish)")
        
        words.append({
            "english": word,
            "turkish": turkish,
            "word_list": "oxford3000",
            "pos": pos,
            "level": level
        })
    
    return words

def extract_oxford_5000_words(text: str) -> List[Dict[str, Any]]:
    """
    Extract Oxford 5000 words from the provided text.
    
    Args:
        text: The text extracted from The Oxford 5000 PDF
        
    Returns:
        A list of dictionaries containing word information
    """
    words = []
    matches = re.findall(OXFORD_5000_PATTERN, text)
    
    for match in matches:
        word = match[0].strip().lower()
        pos = match[1].strip()
        level = match[2].strip()
        
        # Get Turkish translation or use placeholder
        turkish = turkish_translations.get(word, f"{word} (Turkish)")
        
        words.append({
            "english": word,
            "turkish": turkish,
            "word_list": "oxford5000",
            "pos": pos,
            "level": level
        })
    
    return words

def save_words_to_json(words: List[Dict[str, Any]], filename: str) -> None:
    """
    Save the extracted words to a JSON file.
    
    Args:
        words: A list of word dictionaries
        filename: The name of the output JSON file
    """
    with open(f"static/data/{filename}", 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(words)} words to static/data/{filename}")

def main():
    # Import the PDF content that has been extracted from the PDFs
    from static.data.oxford_pdf_content import OXFORD_3000_CONTENT, OXFORD_5000_CONTENT
    
    # Extract words from the texts
    oxford_3000_words = extract_oxford_3000_words(OXFORD_3000_CONTENT)
    oxford_5000_words = extract_oxford_5000_words(OXFORD_5000_CONTENT)
    
    # Save to JSON files
    save_words_to_json(oxford_3000_words, "oxford3000_new.json")
    save_words_to_json(oxford_5000_words, "oxford5000_new.json")
    
    # Create combined wordlist
    combined_words = oxford_3000_words + oxford_5000_words
    save_words_to_json(combined_words, "combined_new.json")
    
    print(f"Total words extracted: {len(combined_words)}")
    
    # Print sample words from each list for verification
    print("\nSample words from Oxford 3000:")
    for word in oxford_3000_words[:10]:
        print(f"{word['english']} ({word['pos']}) - {word['turkish']} - Level: {word['level']}")
    
    print("\nSample words from Oxford 5000:")
    for word in oxford_5000_words[:10]:
        print(f"{word['english']} ({word['pos']}) - {word['turkish']} - Level: {word['level']}")

if __name__ == "__main__":
    main()