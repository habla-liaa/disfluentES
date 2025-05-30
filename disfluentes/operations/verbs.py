from typing import Dict, Optional, Tuple
from IPython import embed
import spacy
from mlconjug3 import Conjugator
from disfluentes.operations import spacy_to_mlconjug3

# Initialize Spanish conjugator
conjugator = Conjugator(language="es")


def get_mlconjug_params(morph: Dict) -> Tuple[str, str, str]:
    """Convert spaCy token morphology to mlconjug3 parameters.

    Args:
        morph: A dictionary with verb morphology information

    Returns:
        Tuple of (mood, tense, person) for mlconjug3
    """

    # Get morphological information
    mood = morph["Mood"]
    tense = morph["Tense"]
    person = morph["Person"]
    number = morph["Number"]
    verb_form = morph["VerbForm"]

    try:
        conjugation = spacy_to_mlconjug3[(verb_form, mood, tense, person, number)]
    except KeyError:
        raise ValueError(f"No conjugation found for morph {morph}")

    mood_mlconjug = conjugation["mood"]
    tense_mlconjug = conjugation["mood"] + " " + conjugation["tense"]
    person_mlconjug = conjugation["person"]

    return mood_mlconjug, tense_mlconjug, person_mlconjug


def conjugate_verb(
    token: spacy.tokens.Token,
    change_person: Optional[str] = None,
    change_number: Optional[str] = None,
    change_tense: Optional[str] = None,
    change_mood: Optional[str] = None,
) -> Optional[str]:
    """Conjugate a Spanish verb using mlconjug3 with optional changes.

    Args:
        token: spaCy token containing a verb
        change_person: New grammatical person (1,2,3)
        change_number: New number (Sing/Plur)
        change_tense: New tense (Pres/Imp/Past/Fut)
        change_mood: New mood (Ind/Sub/Imp)

    Returns:
        Conjugated verb form or None if conjugation fails
    """
    if token.pos_ not in ["VERB", "AUX"]:
        return None

    morph = token.morph.to_dict()

    # Get base infinitive form
    infinitive = token.lemma_

    if " " in infinitive:
        infinitive = infinitive.split(" ")[0]
    
    elif "aste" in infinitive:
        infinitive = infinitive.replace("aste", "ar")
        morph = {
            "Mood": "Ind",
            "Tense": "Past",
            "Person": "2",
            "Number": "Sing",
            "VerbForm": "Fin",
        }
    elif infinitive[-1] != "r":
        infinitive += "r"    

    verb_form = morph["VerbForm"]
    if verb_form != "Inf" and verb_form != "Ger":
        if "Mood" not in morph:
            mood = "Ind"
        else:
            mood = morph["Mood"]
        if "Tense" not in morph:
            tense = "Pres"
        else:
            tense = morph["Tense"]
        if "Person" not in morph:
            person = "1"
        else:
            person = morph["Person"]
        if "Number" not in morph:
            number = "Sing"
        else:
            number = morph["Number"]
        # Exception because of the way argentinian Spanish is conjugated
        if change_person:
            if number == "Plur" and change_person in ["2", "3"]:
                change_person = "1"

        if change_person:
            if number == "Plur" and change_person == "1":
                change_person = "3"

    try:
        # Apply requested changes
        if change_person:
            person = change_person
        if change_number:
            number = change_number
        if change_tense:
            tense = change_tense
        if change_mood:
            mood = change_mood

        morph = {
            "Mood": mood,
            "Tense": tense,
            "Person": person,
            "Number": number,
            "VerbForm": "Fin",
        }

        # Exceptions
        if mood == "Imp" and tense == "Fut":
            morph["Mood"] = "Ind"

        if mood == "Sub" and tense == "Past":
            morph["Tense"] = "Imp"

        if mood == "Imp" and tense == "Imp":
            morph["Mood"] = "Ind"

        mood_mlconjug, tense_mlconjug, person_mlconjug = get_mlconjug_params(morph)

        # Get conjugation table
        verb_conj = conjugator.conjugate(infinitive)

        # Get specific conjugation
        conjugation = verb_conj.conjug_info[mood_mlconjug][tense_mlconjug][
            person_mlconjug
        ]
        if conjugation is None:
            return token.text
        return conjugation

    except Exception as e:
        print(f"Error conjugating verb {infinitive}: {str(e)}")
        return token.text
