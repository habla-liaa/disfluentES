from typing import Dict, Optional, Tuple
from IPython import embed
import spacy
from mlconjug3 import Conjugator
from src.utils.verb_forms_map import spacy_to_mlconjug3

# Initialize Spanish conjugator
conjugator = Conjugator(language='es')

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
    tense_mlconjug = conjugation["mood"] + " "+conjugation["tense"]
    person_mlconjug = conjugation["person"]

    return mood_mlconjug, tense_mlconjug, person_mlconjug

def conjugate_verb(token: spacy.tokens.Token, 
                  change_person: Optional[str] = None,
                  change_number: Optional[str] = None,
                  change_tense: Optional[str] = None,
                  change_mood: Optional[str] = None) -> Optional[str]:
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
        
    # Get base infinitive form
    infinitive = token.lemma_
    morph = token.morph.to_dict()
    
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
            "VerbForm": "Fin"
        }

        mood_mlconjug, tense_mlconjug, person_mlconjug = get_mlconjug_params(morph)

        # Get conjugation table
        verb_conj = conjugator.conjugate(infinitive)
        
        # Get specific conjugation
        conjugation = verb_conj.conjug_info[mood_mlconjug][tense_mlconjug][person_mlconjug]
        
        return conjugation
        
    except Exception as e:
        print(f"Error conjugating verb {infinitive}: {str(e)}")
        return None 