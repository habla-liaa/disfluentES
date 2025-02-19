import re
from typing import Union
from IPython import embed
import spacy
from transformers.models.whisper.english_normalizer import BasicTextNormalizer

normalizer = BasicTextNormalizer()

def clean_word(word: str) -> str:
    if isinstance(word, Union[int, float]):
        word = str(word)
    
    # remove punctuation, numbers, grave accents and unexcepted ASCII characters
    try:
        word = normalizer(word).lower().strip()
    except Exception as e:
        embed()
    word = re.sub(r'\d+', '', word)
    word = re.sub(r'[^\w\s]', '', word)
    word = ''.join(char for char in word if char not in ['à', 'è', 'ì', 'ò', 'ù', 'ã', 'õ', 'ũ', 'ĩ', 'ẽ', 'у', 'н', 'б','ö', 'й','ç'])
    return word
