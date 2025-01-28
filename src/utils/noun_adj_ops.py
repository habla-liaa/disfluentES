from typing import Dict, Optional, Tuple
from IPython import embed
import spacy

vowels = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú']
accented_vowels = ['á', 'é', 'í', 'ó', 'ú']



def to_plural(word):
    # Handle empty words
    if not word:
        return word
        
    # Get the last character
    last_char = word[-1].lower()
    
    # Rule 1: Words ending in vowels (a, e, i, o, u) add 's'
    if last_char in vowels and last_char not in ['í', 'ú']:
        return word + 's'
    
    # Rule 2: Words ending in 'z' change to 'c' and add 'es'
    if last_char == 'z':
        return word[:-1] + 'ces'
    
    # Rule 3: Words ending in 's' or 'x' remain unchanged (when they are llanas/paroxytone)
    if last_char in ['s', 'x'] and word[-2].lower() not in accented_vowels:
        return word
    
    # Rule 4: Words ending in 'í' or 'ú' can take either 's' or 'es'
    # We'll return only 'es' for simplicity
    if last_char in ['í', 'ú']:
        return word + 'es'
    
    # Rule 5: Words ending in other consonants add 'es'
    return word + 'es'

def to_singular(word):
    # Handle empty words
    if not word:
        return word
        
    # no agarra palabras invariables tipo crisis, lunes, tórax, cosmos, etc. 
        
    # Rule 1: Words ending in 's' after a vowel
    if word.endswith('s') and len(word) > 1 and word[-2] in vowels:
        return word[:-1]
        
    # Rule 3: Words ending in 'ces' change to 'z'
    if word.endswith('ces'):
        return word[:-3] + 'z'
        
    # Rule 2: Words ending in 'es'
    if word.endswith('es'):
        # Rule 5: Special case for words with 'í' or 'ú'
        if word.endswith('íes'):
            return word[:-3]
        if word.endswith('úes'):
            return word[:-3]
        return word[:-2]
        
    # If word ends in 's' (after checking other rules)
    if word.endswith('s'):
        return word[:-1]
        
    return word

def to_masculine(word):
    # if word ends in 'a' or 'o' change to 'o'
    if word.endswith('a'):
        return word[:-1] + 'o'
    if word.endswith('as'):
        return word[:-2] + 'os'
    return word

def to_feminine(word):
    # if word ends in 'o' change to 'a'
    if word.endswith('o'):
        return word[:-1] + 'a'
    if word.endswith('os'):
        return word[:-2] + 'as'
    return word
