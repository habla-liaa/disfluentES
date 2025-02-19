"""Functions to generate word variations based on different disfluency types."""

from IPython import embed
import spacy
from typing import List, Set
from .text import get_similar_words, do_substitution
from .verbs import conjugate_verb
from .noun_adj import to_plural, to_singular, to_masculine, to_feminine
from .utils import clean_word

def get_word_variations(
    word: str,
    disfluency_type: str,
    nlp: spacy.language.Language,
    similarity_params: dict = None,
    adj_inflection_probs: dict = None,
    verb_conjugation_probs: dict = None,
    articles_map: dict = None,
    prepositions: list = None,
    conjunctions: dict = None,
) -> Set[str]:
    """Generate all possible variations of a word based on the disfluency type.
    
    Args:
        word: Input word to generate variations for
        disfluency_type: Type of disfluency to apply ('inflection', 'similarity', etc.)
        nlp: Loaded spacy model
        similarity_params: Parameters for similarity search
        adj_inflection_probs: Probabilities for adjective inflections
        verb_conjugation_probs: Probabilities for verb conjugations
        articles_map: Mapping for articles
        prepositions: List of prepositions
        conjunctions: Dictionary of conjunctions
        
    Returns:
        Set of unique word variations
    """
    doc = nlp(word)
    token = doc[0]
    variations = set()
    
    if "inflection" in disfluency_type:
        if token.pos_ == "VERB" or token.pos_ == "AUX":
            # Generate all possible verb conjugations
            morph = token.morph.to_dict()
            numbers = ["Sing", "Plur"]
            tenses = ["Pres", "Imp", "Past", "Fut"]
            moods = ["Ind", "Sub", "Imp"]
            persons = ["1", "2", "3"]
            
            for number in numbers:
                for tense in tenses:
                    for mood in moods:
                        for person in persons:
                            try:
                                conj = conjugate_verb(
                                    token,
                                    change_number=number,
                                    change_tense=tense,
                                    change_mood=mood,
                                    change_person=person
                                )
                                if conj:
                                    variations.add(clean_word(conj))
                            except:
                                continue
                                
        elif token.pos_ == "NOUN":
            # Generate singular/plural forms
            variations.add(clean_word(to_plural(token.text)))
            variations.add(clean_word(to_singular(token.text)))
            
        elif token.pos_ == "ADJ":
            # Generate gender and number variations
            variations.add(clean_word(to_masculine(token.text)))
            variations.add(clean_word(to_feminine(token.text)))
            variations.add(clean_word(to_plural(token.text)))
            variations.add(clean_word(to_singular(token.text)))
            
    if "similarity" in disfluency_type:
        # Get similar words by vector and lemma
        similar = get_similar_words(
            token,
            nlp,
            **(similarity_params or {})
        )
        variations.update(similar)
        
        # Add lemma-based variations
        lemma_doc = nlp(token.lemma_)
        for word_ in nlp.vocab:
            if word_.is_alpha and len(word_.text) > 1:
                if hasattr(word_, "lemma_"):
                    if word_.lemma_ == token.lemma_:
                        variations.add(clean_word(word_.text))
                else:
                    if word_.text == token.lemma_:                        
                        variations.add(clean_word(word_.text))
    
    # Remove empty strings and original word
    variations.discard("")
    variations.discard(clean_word(word))
    
    return variations 