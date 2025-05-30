"""Text operations for Spanish disfluency generation."""

import copy
import random
from IPython import embed
import spacy
from typing import Union
from difflib import get_close_matches
from .utils import clean_word
from .verbs import conjugate_verb
from .noun_adj import to_plural, to_singular, to_masculine, to_feminine
from .phonological import misspell_word
import silabeador

def cut_word(
    word: spacy.tokens.Doc,
    cut_from_start: Union[bool, None] = None,
    chars: bool = False,
) -> str:
    """Remove a random number of syllables from the word beginning or end and return the word"""

    if chars:
        units = list(word.text)
    else:
        units = silabeador.syllabify(word.text)
        if units[0] not in word.text:
            print("cut_word syllables", units, word.text)
            embed()

    if not units:
        return str(word)  # Return the original word if no syllables are found

    # Decide whether to cut from the beginning or the end
    if cut_from_start is None:
        cut_from_start = random.choice([True, False])

    if len(units) > 2:
        num_units_to_cut = random.randint(1, len(units) - 1)
    else:
        num_units_to_cut = 1

    if cut_from_start:
        # Cut from the beginning
        new_word = "".join(units[num_units_to_cut:])
    else:
        # Cut from the end
        new_word = "".join(units[:-num_units_to_cut])

    if new_word == "h":
        new_word = ''.join(units[0:2])

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
    # clean similar words and remove duplicates and original word
    similar_words = [clean_word(word) for word in similar_words]
    similar_words = list(set(similar_words))
    similar_words.remove(word.text.lower()) 

    similar_word = random.choice(similar_words).lower()   

    return similar_word

# TODO Put elsewhere
pronouns_interrogative = ["qué", "cómo", "cuándo", "dónde"]
conj_adv = ["que", "como", "cuando", "donde", "porque"]
rescue_words = ["muchas", "mucho", "mucho", "mucha", "muchos", "muchos", "muchos", "muchos", ]

def do_substitution(
    word: spacy.tokens.Token,
    sub_type: str,
    nlp: spacy.language.Language,
    adj_inflection_probs: dict,
    verb_conjugation_probs: dict,
    substitution_similarity_params: dict,
    char_patterns: dict,
    articles_map: dict,
    prepositions: list,
    conjunctions: dict,
) -> str:
    if word.text.lower() in pronouns_interrogative:
        copy_pronouns_interrogative = copy.deepcopy(pronouns_interrogative)
        copy_pronouns_interrogative.remove(word.text.lower())
        substitute = random.choice(copy_pronouns_interrogative)
    elif word.text.lower() in conj_adv:
        copy_conj_adv = copy.deepcopy(conj_adv)
        copy_conj_adv.remove(word.text.lower())
        substitute = random.choice(conj_adv)
    elif (word.pos_ in ["VERB", "AUX", "NOUN", "ADJ"] or word.text.lower() in rescue_words) and sub_type == "inflection":
        substitute = do_inflection(word, adj_inflection_probs, verb_conjugation_probs)        
    elif word.pos_ in ["VERB", "AUX", "NOUN", "ADJ"] and (sub_type == "similarity" or sub_type == "nominalization"):
        substitute = do_similarity(word, nlp, **substitution_similarity_params)
    elif word.pos_ in (["VERB", "AUX", "NOUN", "ADJ", "ADV"] or word.text.lower() in rescue_words) and sub_type == "misspelling":        
        substitute = misspell_word(word, char_patterns)
    elif word.pos_ in ["DET", "PRON"]:
        if word.text.lower() in articles_map:
            substitute = random.choice(articles_map[word.text.lower()])
        else:
            raise ValueError(f"Det map not found for {word.text}")
    elif word.pos_ == "ADP":
        if word.text in prepositions:
            available_preps = [p for p in prepositions if p != word.text]
            substitute = random.choice(available_preps)
        else:
            substitute = random.choice(prepositions)
    elif word.pos_ == "CCONJ":
        if word.text in conjunctions["CCONJ"]:
            available_conjunctions = [
                c for c in conjunctions["CCONJ"] if c != word.text
            ]
            substitute = random.choice(available_conjunctions)
        else:
            substitute = random.choice(conjunctions["CCONJ"])
    elif word.pos_ == "SCONJ":
        if word.text in conjunctions["SCONJ"]:
            available_conjunctions = [
                c for c in conjunctions["SCONJ"] if c != word.text
            ]
            substitute = random.choice(available_conjunctions)
        else:
            substitute = random.choice(conjunctions["SCONJ"])
    else:
        print("Substitution type not found for", word.pos_, "sub_type", sub_type)
        substitute = word.text
    return substitute


def do_inflection(
    word: spacy.tokens.Doc, adj_inflection_probs: dict, verb_conjugation_probs: dict
) -> str:
    """Inflect a word based on its morphological features."""

    morph = word.morph.to_dict()

    # If noun, change number
    if word.pos_ == "NOUN" or word.text.lower() in rescue_words:
        if "Number" not in morph:
            number = "Sing"
            print("No number found for", word.text, morph)
        else:
            number = morph["Number"]
        if number == "Sing":
            return to_plural(word.text)
        else:
            return to_singular(word.text)
        
    if word.pos_ == "PRON":
        change_gender_or_number = random.choices(
                list(adj_inflection_probs.keys()), weights=adj_inflection_probs.values()
            )[0]
        if change_gender_or_number == "gender":
            if word.text == "el":
                return "la"
            elif word.text == "la":
                return "el"
            elif word.text == "los":
                return "las"
            elif word.text == "las":
                return "los"
            elif word.text == "un":
                return "una"
            elif word.text == "una":
                return "un"
            else:
                return word.text
        else:
            return word.text

    if word.pos_ == "ADJ":

        if "Gender" not in morph:
            change_gender_or_number = "number"
        elif "Number" not in morph:
            change_gender_or_number = "gender"
        else:
            change_gender_or_number = random.choices(
                list(adj_inflection_probs.keys()), weights=adj_inflection_probs.values()
            )[0]

        if change_gender_or_number == "gender":
            return (
                to_masculine(word.text)
                if morph["Gender"] == "Masc"
                else to_feminine(word.text)
            )
        else:
            if "Number" not in morph:
                number = "Sing"
                print("No number found for", word.text, morph)
            else:
                number = morph["Number"]
            return (
                to_plural(word.text)
                if number == "Plur"
                else to_singular(word.text)
            )

    # If verb, inflect verb form
    if word.pos_ in ["VERB", "AUX"]:

        # if gerundio conjugate verb to any random form
        if morph["VerbForm"] == "Ger" or morph["VerbForm"] == "Inf":
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
            if "Person" not in morph:
                original_person = "1"
                print("No person found for", word.text, morph)
            else:
                original_person = morph["Person"][0]
            persons = ["1", "2", "3"]
            persons.remove(original_person)
            person = random.choice(persons)
            return conjugate_verb(word, change_person=person)
        elif change_type == "change_tense":
            tense = "Past" if "Pres" in morph["Tense"] else "Pres"
            return conjugate_verb(word, change_tense=tense)
        elif change_type == "change_mood":
            return conjugate_verb(word, change_mood="Sub")
        elif change_type == "infinitive":
            return str(word.lemma_)
        else:
            print("Inflection type not found for", word.text, morph)
            return word.text



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
        ms = nlp.vocab.vectors.most_similar(word.vector[None].copy(), n=n_words)
        similar_words.update([nlp.vocab.strings[w] for w in ms[0][0]])

    # Add phonologically similar words
    all_words = [w for w in nlp.vocab.strings if len(w) > 2]
    if close_matches:
        phono_similar = get_close_matches(word.text, all_words, cutoff=cutoff)
        similar_words.update(phono_similar)

    # Remove original word
    similar_words.discard(word)

    return sorted(list(similar_words))
