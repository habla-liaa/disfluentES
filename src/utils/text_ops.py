"""Text operations for Spanish disfluency generation."""

import random
import gin
import spacy

def cut_word(word: spacy.tokens.Doc) -> str:
    """Remove a random number of syllables from the word beginning or end and return the word"""

    syllables = word._.syllables
    if not syllables:
        return str(word)  # Return the original word if no syllables are found

    # Decide whether to cut from the beginning or the end
    cut_from_start = random.choice([True, False])
    num_syllables_to_cut = random.randint(1, len(syllables)-1)

    if cut_from_start:
        # Cut from the beginning
        new_word = ''.join(syllables[num_syllables_to_cut:])
    else:
        # Cut from the end
        new_word = ''.join(syllables[:-num_syllables_to_cut])

    return new_word


@gin.configurable
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


@gin.configurable
def repeat_word(sentence: str, pos_tag: dict) -> tuple[str, bool]:
    """Repeat a word in the sentence based on its POS tag."""
    words = sentence.split()
    if not words:
        return sentence, False
        
    # Select word based on POS tag probabilities
    word_idx = random.randint(0, len(words)-1)
    word_to_repeat = words[word_idx]
    
    # Insert immediately before
    words.insert(word_idx, word_to_repeat)
    return ' '.join(words), True


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