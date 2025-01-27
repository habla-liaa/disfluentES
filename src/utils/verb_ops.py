import random
from typing import Dict, Optional, Tuple
from IPython import embed
import spacy
from mlconjug3 import Conjugator
import pickle

# Initialize Spanish conjugator
conjugator = Conjugator(language='es')

# Load spacy_to_mlconjug3
with open("scripts/spacy_to_mlconjug3.pkl", "rb") as f:
    spacy_to_mlconjug3 = pickle.load(f)


# Map spaCy person to mlconjug3 person
person_map = {
        "1": {"Sing": "yo", "Plur": "nosotros"},
        "2": {"Sing": "tú", "Plur": "vosotros"},
        "3": {"Sing": "él", "Plur": "ellos"}
    }

# Map spaCy person and number to mlconjug3 person
person_number_map = {
                ("1", "Sing"): "yo",
                ("2", "Sing"): "tú", 
                ("3", "Sing"): "él",
                ("1", "Plur"): "nosotros",
                ("2", "Plur"): "vosotros",
                ("3", "Plur"): "ellos"
            }

def get_mlconjug_params(token: spacy.tokens.Token) -> Tuple[str, str, str]:
    """Convert spaCy token morphology to mlconjug3 parameters.
    
    Args:
        token: A spaCy token with verb morphology information
        
    Returns:
        Tuple of (mood, tense, person) for mlconjug3
    """
    
    # Get morphological information
    morph = token.morph.to_dict()    
    
    # Get mood
    if "Mood" in morph and "Tense" in morph:
        canditates = spacy_to_mlconjug3[(morph["Mood"], morph["Tense"])]    
    
        peak = random.choice(canditates)
        tense =peak['mood'] + peak['verb_form']
        mood = peak['mood']
    else:        
        raise ValueError(f"No mood or tense found for {token.text} with morph {morph}")
    
    # Get person
    if "Person" in morph and "Number" in morph:
        person_num = morph["Person"]
        number = morph["Number"]
        person = person_map[person_num][number]
    else:
        raise ValueError(f"No person or number found for {token.text} with morph {morph}")
    
    return mood, tense, person

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
        # Get current morphological information
        mood, tense, person = get_mlconjug_params(token)
        
        # Apply requested changes
        if change_person and change_number:
            person = person_number_map.get((change_person, change_number), person)

        if change_tense:    
            candidates = spacy_to_mlconjug3[(mood, change_tense)]    
            peak = random.choice(candidates)
            tense = peak['mood'] + peak['verb_form']

        if change_mood:
            candidates = spacy_to_mlconjug3[(change_mood, tense)]    
            peak = random.choice(candidates)
            mood = peak['mood']
        
        # Get conjugation table
        verb_conj = conjugator.conjugate(infinitive)
        
        # Get specific conjugation
        conjugation = verb_conj.conjug_info[mood][tense][person]
        
        return conjugation
        
    except Exception as e:
        print(f"Error conjugating verb {infinitive}: {str(e)}")
        return None 