"""Text operations for Spanish disfluency generation."""

import random
import gin
import spacy
<<<<<<< HEAD
from difflib import get_close_matches
=======

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
>>>>>>> dd45405e142cd3babf9945ff28fa8018b6fc66bf


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

@gin.configurable
def get_similar_words(word: str, n_words: int =10) -> list:
   nlp = spacy.load("es_core_news_lg") # esto debería estar afuera
   doc = nlp(word)
   token = doc[0]
   
   similar_words = set()
   
   # Get word vector neighbors from model's vocabulary
   if token.has_vector:
       ms = nlp.vocab.vectors.most_similar(
           token.vector[None], n=n_words
       )
       similar_words.update([nlp.vocab.strings[w] for w in ms[0][0]])
       
   # Add phonologically similar words
   all_words = [w for w in nlp.vocab.strings if len(w) > 2]
   phono_similar = get_close_matches(word, all_words, n=10, cutoff=0.8)
   similar_words.update(phono_similar)
   
   # Remove original word
   similar_words.discard(word)
   
   return sorted(list(similar_words))