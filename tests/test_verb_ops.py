import pytest
import spacy
from src.operations.verbs import get_mlconjug_params, conjugate_verb

# Initialize spaCy
nlp = spacy.load('es_core_news_lg')

'''
@pytest.fixture
def verb_tokens():
    """Fixture providing various Spanish verb tokens for testing"""
    verbs = {
        'present_1s': nlp('pienso')[0],  # 1st person singular present
        'present_3s': nlp('piensa')[0],  # 3rd person singular present
        'imperfect_2s': nlp('piensas')[0],  # 2nd person singular imperfect
        'future_1p': nlp('piensaremos')[0],  # 1st person plural future
        'subjunctive_3p': nlp('piensan')[0],  # 3rd person plural subjunctive
    }
    return verbs
'''

def test_get_mlconjug_params_present_ind():
    """Test get_mlconjug_params with present tense verb"""
    token = nlp('pienso')[0]  # 1st person singular present indicativo
    print(token.morph.to_dict())
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    print(mood, tense, person)
    assert mood == 'Indicativo'
    assert 'presente' in tense
    assert person == 'yo'

def test_get_mlconjug_params_imperfect_ind():
    """Test get_mlconjug_params with imperfect tense verb"""
    token = nlp('comía')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Indicativo'
    assert 'imperfecto' in tense
    assert person == 'él'

def test_get_mlconjug_params_perfect_ind():
    """Test get_mlconjug_params with past perfect tense verb"""
    token = nlp('comí')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Indicativo'
    assert 'perfecto' in tense
    assert person == 'yo'

def test_get_mlconjug_params_future_ind():
    """Test get_mlconjug_params with future tense verb"""
    token = nlp('comeremos')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Indicativo'
    assert 'futuro' in tense
    assert person == 'nosotros'

def test_get_mlconjug_params_present_sub():
    """Test get_mlconjug_params with present tense verb"""
    token = nlp('camine')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Subjuntivo'
    assert 'presente' in tense
    assert person == 'él' # también puede ser 'yo' o 'usted'

def test_get_mlconjug_params_imp1_sub():
    """Test get_mlconjug_params with present tense verb"""
    token = nlp('caminara')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Subjuntivo'
    assert 'imperfecto 1' in tense
    assert person == 'él' # también puede ser 'yo' o 'usted'


def test_get_mlconjug_params_imp2_sub():
    """Test get_mlconjug_params with present tense verb"""
    token = nlp('caminasen')[0]  
    mood, tense, person = get_mlconjug_params(token.morph.to_dict())
    assert mood == 'Subjuntivo'
    assert 'imperfecto 1' in tense
    assert person == 'ellos' # también puede ser 'yo' o 'usted'

    
# def test_get_mlconjug_params_invalid():
#     """Test get_mlconjug_params with non-verb token"""
#     token = nlp('casa')[0]  # noun
#     with pytest.raises(ValueError):
#         get_mlconjug_params(token)

# def test_conjugate_verb_no_changes(verb_tokens):
#     """Test conjugate_verb without any changes"""
#     result = conjugate_verb(verb_tokens['present_1s'])
#     assert result == 'como'

# def test_conjugate_verb_change_person():
#     """Test conjugate_verb with person change"""
#     token = nlp('como')[0]  # 1st person singular
#     result = conjugate_verb(token, change_person='2')
#     assert result == 'comes'  # 2nd person singular

# def test_conjugate_verb_change_number():
#     """Test conjugate_verb with number change"""
#     token = nlp('come')[0]  # 3rd person singular
#     result = conjugate_verb(token, change_number='Plur')
#     assert result == 'comen'  # 3rd person plural

# def test_conjugate_verb_change_tense():
#     """Test conjugate_verb with tense change"""
#     token = nlp('como')[0]  # present tense
#     result = conjugate_verb(token, change_tense='Past')
#     assert result in ['comí', 'comía']  # past tense forms

# def test_conjugate_verb_change_mood():
#     """Test conjugate_verb with mood change"""
#     token = nlp('come')[0]  # indicative mood
#     result = conjugate_verb(token, change_mood='Sub')
#     assert result == 'coma'  # subjunctive mood

# def test_conjugate_verb_multiple_changes():
#     """Test conjugate_verb with multiple changes"""
#     token = nlp('como')[0]  # 1st person singular present
#     result = conjugate_verb(
#         token,
#         change_person='3',
#         change_number='Plur',
#         change_tense='Past'
#     )
#     assert result in ['comieron', 'comían']  # 3rd person plural past

# def test_conjugate_verb_non_verb():
#     """Test conjugate_verb with non-verb token"""
#     token = nlp('casa')[0]  # noun
#     result = conjugate_verb(token)
#     assert result is None 