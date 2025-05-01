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

def process_oxford_3000_pdf():
    """Process the Oxford 3000 PDF content"""
    
    # Since we can't directly read the PDF in this environment,
    # we'll use the text from the first few pages provided by the user
    oxford_3000_content = """
    The Oxford 3000™
    The Oxford 3000 is the list of the 3000 most important words to learn in English, from A1 to B2 level.

    a, an indefinite article A1      aged adj. B1                      anyway adv. A2                attend v. A2
    abandon v. B2                    agency n. B2                      anywhere adv., pron. A2       attention n., exclam. A2
    ability n. A2                    agenda n. B2                      apart adv. B1                 attitude n. B1
    able adj. A2                     agent n. B1                       apartment n. A1               attract v. B1
    about prep., adv. A1             aggressive adj. B2                apologize v. B1               attraction n. B1
    above prep., adv. A1             ago adv. A1                       app n. A2                     attractive adj. A2
    abroad adv. A2                   agree v. A1                       apparent adj. B2              audience n. A2
    absolute adj. B2                 agreement n. B1                   apparently adv. B2            August n. A1
    absolutely adv. B1               ah exclam. A2                     appeal n., v. B2              aunt n. A1
    academic adj.B1, n. B2           ahead adv. B1                     appear v. A2                  author n. A2
    accept v. A2                     aid n., v. B2                     appearance n. A2              authority n. B1
    acceptable adj. B2               aim v., n. B1                     apple n. A1                   autumn n. A1
    access n., v. B1                 air n. A1                         application n. B1             available adj. A2
    accident n. A2                   aircraft n. B2                    apply v. A2                   average adj., n. A2, v. B1
    accommodation n. B1              airline n. A2                     appointment n. B1             avoid v. A2
    accompany v. B2                  airport n. A1                     appreciate v. B1              award n. A2, v. B1
    according to prep. A2            alarm n. B1, v. B2                approach n., v. B2            aware adj. B1
    account n. B1, v. B2             album n. B1                       appropriate adj. B2           away adv. A1
    accurate adj. B2                 alcohol n. B1                     approval n. B2                awful adj. A2
    accuse v. B2                     alcoholic adj. B1                 approve v. B2                 baby n. A1
    achieve v. A2                    alive adj. A2                     approximately adv. B1         back n., adv. A1, adj. A2, v. B2
    achievement n. B1                all det., pron. A1, adv. A2       April n. A1                   background n. A2
    acknowledge v. B2                all right adj./adv., exclam. A2   architect n. A2               backwards adv. B1
    acquire v. B2                    allow v. A2                       architecture n. A2            bacteria n. B2
    across prep., adv. A1            almost adv. A2                    area n. A1                    bad adj. A1
    act v. A2, n. B1                 alone adj./adv. A2                argue v. A2                   badly adv. A2
    action n. A1                     along prep., adv. A2              argument n. A2                bag n. A1
    active adj. A2                   already adv. A2                   arise v. B2                   bake v. B1
    activity n. A1                   also adv. A1                      arm n. A1                     balance n., v. B1
    actor n. A1                      alter v. B2                       armed adj. B2                 ball n. A1
    actress n. A1                    alternative n. A2, adj. B1        arms n. B2                    ban v., n. B1
    actual adj. B2                   although conj. A2                 army n. A2                    banana n. A1
    actually adv. A2                 always adv. A1                    around prep., adv. A1         band n. A1
    ad n. B1                         amazed adj. B1                    arrange v. A2                 bank (money) n. A1
    adapt v. B2                      amazing adj. A1                   arrangement n. A2             bank (river) n. B1
    add v. A1                        ambition n. B1                    arrest v., n. B1              bar n. A2, v. B2
    addition n. B1                   ambitious adj. B1                 arrival n. B1                 barrier n. B2
    additional adj. B2               among prep. A2                    arrive v. A1                  base n., v. B1
    address n. A1, v. B2             amount n. A2, v. B2               art n. A1                     baseball n. A2
    administration n. B2             analyse v. B1                     article n. A1                 based adj. A2
    admire v. B1                     analysis n. B1                    artificial adj. B2            basic adj. B1
    admit v. B1                      ancient adj. A2                   artist n. A1                  basically adv. B2
    adopt v. B2                      and conj. A1                      artistic adj. B2              basis n. B1
    adult n. A1, adj. A2             anger n. B2                       as prep. A1, adv., conj. A2   basketball n. A2
    advance n., v., adj. B2          angle n. B2                       ashamed adj. B2               bath n. A1
    advanced adj. B1                 angry adj. A1                     ask v. A1                     bathroom n. A1
    advantage n. A2                  animal n. A1                      asleep adj. A2                battery n. B1
    adventure n. A2                  ankle n. A2                       aspect n. B2                  battle n. B1, v. B2
    advertise v. A2                  anniversary n. B2                 assess v. B2                  be v., auxiliary v. A1
    advertisement n. A2              announce v. B1                    assessment n. B2              beach n. A1
    advertising n. A2                announcement n. B1                assignment n. B1              bean n. A2
    advice n. A1                     annoy v. B1                       assist v. B1                  bear (deal with) v. B2
    advise v. B1                     annoyed adj. B1                   assistant n., adj. A2         bear (animal) n. A2
    affair n. B2                     annoying adj. B1                  associate v. B2               beat v. A2, n. B2
    affect v. A2                     annual adj. B2                    associated adj. B2            beautiful adj. A1
    afford v. B1                     another det./pron. A1             association n. B2             beauty n. B1
    afraid adj. A1                   answer n., v. A1                  assume v. B2                  because conj. A1
    after prep. A1, conj., adv. A2   anxious adj. B2                   at prep. A1                   become v. A1
    afternoon n. A1                  any det., pron. A1, adv. A2       athlete n. A2                 bed n. A1
    afterwards adv. B2               anybody pron. A2                  atmosphere n. B1              bedroom n. A1
    again adv. A1                    any more adv. A2                  attach v. B1                  bee n. B1
    against prep. A2                 anyone pron. A1                   attack n., v. A2              beef n. A2
    age n. A1, v. B1                 anything pron. A1                 attempt n., v. B2             beer n. A1
    """
    
    return oxford_3000_content

def process_oxford_5000_pdf():
    """Process the Oxford 5000 PDF content"""
    
    # Since we can't directly read the PDF in this environment,
    # we'll use the text from the first few pages provided by the user
    oxford_5000_content = """
    The Oxford 5000™ (American English)
    The Oxford 5000 is an expanded core word list for advanced learners of English. As well as the Oxford
    3000, it includes an additional 2000 words for learners at B2-C1 level, which are listed here.

    abolish v. C1                AIDS n. B2                    assembly n. C1                besides prep., adv. B2
    abortion n. C1               alert v., n., adj. C1         assert v. C1                  betray v. C1
    absence n. C1                alien n. B2, adj. C1          assertion n. C1               beverage n. C1
    absent adj. C1               align v. C1                   asset n. B2                   bias n. B2
    absorb v. B2                 alignment n. C1               assign v. B2                  bid n., v. B2
    abstract adj. B2             alike adv., adj. C1           assistance n. B2              bind v. C1
    absurd adj. C1               allegation n. C1              assumption n. B2              biography n. C1
    abuse n., v. C1              allege v. C1                  assurance n. C1               biological adj. B2
    academy n. C1                allegedly adv. C1             assure v. B2                  bishop n. C1
    accelerate v. C1             alliance n. C1                astonishing adj. B2           bizarre adj. C1
    accent n. B2                 allocate v. C1                asylum n. C1                  blade n. C1
    acceptance n. C1             allocation n. C1              athletic adj. B2              blanket n. B2
    accessible adj. C1           allowance n. C1               atrocity n. C1                blast n., v. C1
    accidentally adv. B2         ally n. C1                    attachment n. B2              bleed v. C1
    accommodate v. B2            alongside prep. B2            attain v. C1                  blend v., n. C1
    accommodation n. B2          altogether adv. B2            attendance n. C1              bless v. C1
    accomplish v. B2             aluminum n. C1                attribute v., n. C1           blessing n. C1
    accomplishment n. C1         amateur adj., n. C1           auction n. C1                 blow n. B2
    accordingly adv. C1          ambassador n. C1              audio adj. B2                 boast v. C1
    accountability n. C1         ambitious adj. B2             audit n. C1                   bold adj. B2
    accountable adj. C1          ambulance n. B2               authentic adj. C1             bombing n. B2
    accountant n. B2             amend v. C1                   authorize v. C1               bonus n. C1
    accumulate v. C1             amendment n. C1               auto n. C1                    booking n. C1
    accumulation n. C1           amid prep. C1                 autonomy n. C1                boom n. C1
    accuracy n. B2               amusing adj. B2               autumn n. C1                  boost v., n. B2
    accurately adv. B2           analogy n. C1                 availability n. C1            bounce v. C1
    accusation n. C1             analyst n. B2                 await v. C1                   bound adj. B2
    accused n. C1                ancestor n. B2                awareness n. B2               boundary n. C1
    acid n. B2, adj. C1          anchor n. C1                  awkward adj. B2               bow1 v., n. C1
    acquisition n. C1            angel n. C1                   backdrop n. C1                breach n., v. C1
    acre n. B2                   animation n. B2               backing n. C1                 breakdown n. C1
    activate v. B2               annually adv. B2              backup n. C1                  breakthrough n. C1
    activation n. C1             anonymous adj. C1             badge n. B2                   breed v., n. C1
    activist n. C1               anticipate v. B2              bail n. C1                    brick n. B2
    acute adj. C1                anxiety n. B2                 balanced adj. B2              briefly adv. B2
    adaptation n. C1             apology n. B2                 ballet n. B2                  broadband n. C1
    addiction n. B2              apparatus n. C1               balloon n. B2                 broadcaster n. B2
    additionally adv. B2         apparel n. C1                 ballot n. C1                  broadly adv. B2
    adequate adj. B2             appealing adj. C1             bankruptcy n. C1              browser n. C1
    adequately adv. B2           appetite n. C1                banner n. C1                  brutal adj. C1
    adhere v. C1                 applaud v. C1                 bare adj. C1                  buck n. B2
    adjacent adj. C1             applicable adj. C1            barely adv. B2                buddy n. C1
    adjust v. B2                 applicant n. B2               bargain n. B2                 buffer n. C1
    adjustment n. C1             appoint v. C1                 barrel n. C1                  bug n. B2
    administer v. C1             appreciation n. C1            basement n. B2                bulk n. C1
    administrative adj. C1       appropriately adv. B2         basket n. B2                  burden n. C1
    administrator n. C1          arbitrary adj. C1             bass1 n. C1                   bureaucracy n. C1
    admission n. C1              architectural adj. C1         bat n. B2, v. C1              burial n. C1
    adolescent n. C1             archive n. C1                 battlefield n. C1             burst v. C1
    adoption n. C1               arena n. C1                   bay n. C1                     cabin n. B2
    adverse adj. C1              arm v. C1                     beam n. C1                    cabinet n. C1
    advocate n., v. C1           array n. C1                   beast n. C1                   calculation n. C1
    aesthetic adj. C1            arrow n. B2                   behalf n. C1                  canal n. B2
    affection n. C1              articulate v. C1              behavioral adj. C1            candle n. B2
    affordable adj. B2           artwork n. B2                 beloved adj. C1               canvas n. C1
    aftermath n. C1              ash n. C1                     bench n. C1                   capability n. C1
    aged adj. B2                 aspiration n. C1              benchmark n. C1               capitalism n. C1
    aggression n. C1             aspire v. C1                  beneath prep. C1              capitalist adj. C1
    agricultural adj. C1         assassination n. C1           beneficial adj. B2            carbon n. B2
    agriculture n. B2            assault n., v. C1             beneficiary n. C1             cargo n. C1
    aide n. C1                   assemble v. C1                beside prep. B2               carriage n. C1
    """
    
    return oxford_5000_content

def main():
    # Process the PDF content
    oxford_3000_text = process_oxford_3000_pdf()
    oxford_5000_text = process_oxford_5000_pdf()
    
    # Extract words from the texts
    oxford_3000_words = extract_oxford_3000_words(oxford_3000_text)
    oxford_5000_words = extract_oxford_5000_words(oxford_5000_text)
    
    # Save to JSON files
    save_words_to_json(oxford_3000_words, "oxford3000_new.json")
    save_words_to_json(oxford_5000_words, "oxford5000_new.json")
    
    # Create combined wordlist
    combined_words = oxford_3000_words + oxford_5000_words
    save_words_to_json(combined_words, "combined_new.json")
    
    print(f"Total words extracted: {len(combined_words)}")
    
    # Print sample words from each list for verification
    print("\nSample words from Oxford 3000:")
    for word in oxford_3000_words[:5]:
        print(f"{word['english']} ({word['pos']}) - {word['turkish']} - Level: {word['level']}")
    
    print("\nSample words from Oxford 5000:")
    for word in oxford_5000_words[:5]:
        print(f"{word['english']} ({word['pos']}) - {word['turkish']} - Level: {word['level']}")

if __name__ == "__main__":
    main()