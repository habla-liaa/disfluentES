"""Text operations for Spanish disfluency generation."""

import random
import spacy
from typing import Union
from difflib import get_close_matches
from src.utils.verb_ops import conjugate_verb


def cut_word(
    word: spacy.tokens.Doc,
    cut_from_start: Union[bool, None] = None,
    chars: bool = False,
) -> str:
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

    num_units_to_cut = random.randint(1, len(units) - 1)

    if cut_from_start:
        # Cut from the beginning
        new_word = "".join(units[num_units_to_cut:])
    else:
        # Cut from the end
        new_word = "".join(units[:-num_units_to_cut])

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
    return " ".join(words)


def repeat_words(sentence: str, idx: int, order: int) -> str:
    """Repeat a word in the sentence based on its index."""
    words = sentence.split()
    if not words:
        return sentence

    words_to_repeat = words[idx : idx + order]
    for i in range(order):
        words.insert(idx, words_to_repeat[-i - 1])

    return " ".join(words)


def do_similarity(
    word: spacy.tokens.Doc,
    nlp: spacy.language.Language,
    n_words: int = 10,
    cutoff: float = 0.8,
    vector_similarity: bool = True,
    close_matches: bool = True,
) -> str:
    """Generate a similar word based on the word's vector."""
    similar_words = get_similar_words(
        word,
        nlp,
        n_words=n_words,
        cutoff=cutoff,
        vector_similarity=vector_similarity,
        close_matches=close_matches,
    )
    return random.choice(similar_words)


def do_inflection(
    word: spacy.tokens.Doc, noun_inflection_probs: dict, verb_conjugation_probs: dict
) -> str:
    """Inflect a word based on its morphological features."""

    morph = word.morph.to_dict()

    # If noun, inflect noun form
    if word.pos_ == "NOUN":
        return inflect_noun(word, noun_inflection_probs)


    # If verb, inflect verb form
    if word.pos_ in ["VERB", "AUX"]:

        # if gerundio conjugate verb to any random form
        if morph["VerbForm"] == "Ger":
            number = random.choice(["Sing", "Plur"])
            tense = random.choice(["Pres", "Imp", "Past", "Fut"])
            mood = random.choice(["Ind", "Sub", "Imp"])
            person = random.choice(["1", "2", "3"])
            return conjugate_verb(
                word,
                change_number=number,
                change_tense=tense,
                change_mood=mood,
                change_person=person,
            )

        change_type = random.choices(
            list(verb_conjugation_probs.keys()), weights=verb_conjugation_probs.values()
        )[0]
        
        if change_type == "change_number":
            number = "Plur" if "Sing" in morph["Number"] else "Sing"
            return conjugate_verb(word, change_number=number)
        elif change_type == "change_person":
            original_person = morph["Person"][0]
            person = random.choice(["1", "2", "3"].pop(original_person))
            return conjugate_verb(word, change_person=person)
        elif change_type == "change_tense":
            tense = "Past" if "Pres" in morph["Tense"] else "Pres"
            return conjugate_verb(word, change_tense=tense)
        elif change_type == "change_mood":
            return conjugate_verb(word, change_mood="Sub")


def insert_article(
    sentence: str, word_idx: int, gender: str, number: str, articles: list
) -> str:
    """Insert an appropriate article before a word based on its gender and number."""
    words = sentence.split()
    if not words or word_idx >= len(words):
        return sentence

    if gender == "fem" and number == "sing":
        article = random.choice(["la", "una"])
    elif gender == "fem" and number == "plur":
        article = random.choice(["las", "unas"])
    elif gender == "masc" and number == "sing":
        article = random.choice(["el", "un"])
    elif gender == "masc" and number == "plur":
        article = random.choice(["los", "unos"])
    else:
        article = random.choice(articles)

    words.insert(word_idx, article)
    return " ".join(words)


def get_similar_words(
    word: spacy.tokens.Doc,
    nlp: spacy.language.Language,
    n_words: int = 10,
    cutoff: float = 0.8,
    vector_similarity: bool = True,
    close_matches: bool = True,
) -> list:

    similar_words = set()

    # Get word vector neighbors from model's vocabulary
    if vector_similarity and word.has_vector:
        ms = nlp.vocab.vectors.most_similar(word.vector[None], n=n_words)
        similar_words.update([nlp.vocab.strings[w] for w in ms[0][0]])

    # Add phonologically similar words
    all_words = [w for w in nlp.vocab.strings if len(w) > 2]
    if close_matches:
        phono_similar = get_close_matches(word, all_words, cutoff=cutoff)
        similar_words.update(phono_similar)

    # Remove original word
    similar_words.discard(word)

    return sorted(list(similar_words))
