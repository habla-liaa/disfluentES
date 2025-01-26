"""Text operations for Spanish disfluency generation."""

import random
import gin
import spacy
from typing import Union


def cut_word(word: spacy.tokens.Doc, cut_from_start: Union[bool, None] = None, chars: bool = False) -> str:
    """Remove a random number of syllables from the word beginning or end and return the word"""

    if chars:
        units = list(word.text)
    else:
        units = word._.syllables
    
    if not units:
        return str(word)  # Return the original word if no syllables are found

    # Decide whether to cut from the beginning or the end
    if cut_from_start is None:
        cut_from_start = random.choice([True, False])

    num_units_to_cut = random.randint(1, len(units)-1)

    if cut_from_start:
        # Cut from the beginning
        new_word = ''.join(units[num_units_to_cut:])
    else:
        # Cut from the end
        new_word = ''.join(units[:-num_units_to_cut])

    return new_word


def insert_filler(sentence: str, fillers: list) -> str:
    """Insert a filler word at a random position in the sentence."""
    if not sentence:
        return sentence
        
    words = sentence.split()
    if not words:
        return sentence
        
    filler = random.choice(fillers)
    insert_pos = random.randint(0, len(words))
    words.insert(insert_pos, filler)
    return ' '.join(words)


def repeat_words(sentence: str, idx: int, order: int) -> str:
    """Repeat a word in the sentence based on its index."""  
    words = sentence.split()
    if not words:
        return sentence
    
    words_to_repeat = words[idx:idx+order]
    for i in range(order):
        words.insert(idx, words_to_repeat[-i-1])

    return ' '.join(words)

def do_similarity(word: spacy.tokens.Doc, sim_threshold: float = 0.5) -> str:
    """Generate a similar word based on the word's vector."""
    raise NotImplementedError

def do_inflection(word: spacy.tokens.Doc, noun_inflection_probs: dict) -> str:
    """Inflect a word based on its morphological features."""
    
    # If verb, inflect verb form
    if word.pos_ in ['VERB', 'AUX']:        
        if word.has_morph() and word.morph.get('VerbForm') == ['Fin']:
            number = 'Sing' if 'Plur' in word.morph.get('Number',[]) else 'Plur'
            inflected = word._.inflect({'Number': number})
            return inflected
        else:
            inflected = word.lemma_ if word.text != word.lemma_ else word._.inflect('VerbForm=Fin')
            return inflected
        
    elif word.pos_ in ['NOUN', 'ADJ']:
        change_type = random.choices(list(noun_inflection_probs.keys()),
                                                     weights=noun_inflection_probs.values())[0]

        if change_type == 'number':
            number = 'Sing' if 'Plur' in word.morph.get('Number',[]) else 'Plur'
            inflected = word._.inflect({'Number': number})
            return inflected
        elif change_type == 'gender':
            gender = 'Fem' if 'Masc' in word.morph.get('Gender', []) else 'Masc'
            inflected = word._.inflect({'Gender': gender})
            return inflected

        
    return word

@gin.configurable
def insert_article(sentence: str, word_idx: int, gender: str, number: str, articles: list) -> str:
    """Insert an appropriate article before a word based on its gender and number."""
    words = sentence.split()
    if not words or word_idx >= len(words):
        return sentence
        
    if gender == 'fem' and number == 'sing':
        article = random.choice(['la', 'una'])
    elif gender == 'fem' and number == 'plur':
        article = random.choice(['las', 'unas'])
    elif gender == 'masc' and number == 'sing':
        article = random.choice(['el', 'un'])
    elif gender == 'masc' and number == 'plur':
        article = random.choice(['los', 'unos'])
    else:
        article = random.choice(articles)
        
    words.insert(word_idx, article)
    return ' '.join(words) 