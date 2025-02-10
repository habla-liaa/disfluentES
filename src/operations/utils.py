import re
from transformers.models.whisper.english_normalizer import BasicTextNormalizer

normalizer = BasicTextNormalizer()

def clean_word(word: str) -> str:
    # remove punctuation, numbers, grave accents and unexcepted ASCII characters
    word = normalizer(word).lower().strip()
    word = re.sub(r'\d+', '', word)
    word = re.sub(r'[^\w\s]', '', word)
    word = ''.join(char for char in word if char not in ['à', 'è', 'ì', 'ò', 'ù', 'ã', 'õ', 'ũ', 'ĩ', 'ẽ'])
    return word
