import pytest
import spacy
import numpy as np
from src.generator import SpanishDisfluencyGenerator

@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    gen = SpanishDisfluencyGenerator()
    return gen

def test_apply_substitution_verb_inflection_number(generator):
    """Test verb substitution with number inflection."""
    text = "los niños corren rápido"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'VERB': 1.0}
    generator.substitution_alteration_subclass = {'inflection': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change verb from plural to singular
    assert result != text
    assert "corre" in result
    assert result.startswith("los niños") and result.endswith("rápido")

def test_apply_substitution_verb_inflection_tense(generator):
    """Test verb substitution with tense inflection."""
    text = "el niño caminando rápido"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'VERB': 1.0}
    generator.substitution_alteration_subclass = {'inflection': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change verb from gerund to finite form
    assert result != text
    assert "caminando" not in result
    assert "camina" in result or "caminó" in result
    assert result.startswith("el niño") and result.endswith("rápido")

def test_apply_substitution_noun_gender(generator):
    """Test noun substitution with gender change."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'NOUN': 1.0}
    generator.substitution_alteration_subclass = {'inflection': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change noun gender
    assert result != text
    assert "gata" in result
    assert result.startswith("el") and result.endswith("negro")

def test_apply_substitution_noun_number(generator):
    """Test noun substitution with number change."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'NOUN': 1.0}
    generator.substitution_alteration_subclass = {'inflection': 1.0}
    np.random.seed(43)  # Different seed to force number change
    result = generator._apply_substitution(text, doc)
    # Should change noun number
    assert result != text
    assert "gatos" in result
    assert result.startswith("el") and result.endswith("negro")

def test_apply_substitution_adjective_gender(generator):
    """Test adjective substitution with gender change."""
    text = "la gata blanca"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'ADJ': 1.0}
    generator.substitution_alteration_subclass = {'inflection': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change adjective gender
    assert result != text
    assert "blanco" in result
    assert result.startswith("la gata")

def test_apply_substitution_determiner_definite_to_indefinite(generator):
    """Test determiner substitution from definite to indefinite."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'DET': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change determiner from el to un
    assert result != text
    assert result.startswith("un gato")

def test_apply_substitution_determiner_indefinite_to_definite(generator):
    """Test determiner substitution from indefinite to definite."""
    text = "un gato negro"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'DET': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should change determiner from un to el
    assert result != text
    assert result.startswith("el gato")

def test_apply_substitution_preposition(generator):
    """Test preposition substitution."""
    text = "voy a casa"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'ADP': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should substitute preposition
    assert result != text
    assert any(prep in result for prep in ['de', 'en', 'por', 'para', 'con', 'sin'])
    assert result.startswith("voy") and result.endswith("casa")

def test_apply_substitution_misspelling(generator):
    """Test misspelling substitution."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'NOUN': 1.0}
    generator.substitution_alteration_subclass = {'misspelling': 1.0}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should introduce character substitution
    assert result != text
    assert result.startswith("el") and result.endswith("negro")
    assert "gato" not in result

def test_apply_substitution_no_candidates(generator):
    """Test substitution when no valid candidates exist."""
    text = "ah eh"  # Interjections
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'VERB': 1.0, 'NOUN': 1.0}
    result = generator._apply_substitution(text, doc)
    # Should apply phonological error to a random word
    assert result != text

def test_apply_substitution_empty_text(generator):
    """Test substitution with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_substitution(text, doc)
    assert result == text

def test_apply_substitution_whitespace(generator):
    """Test substitution with whitespace."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_substitution(text, doc)
    assert result == text

def test_apply_substitution_multiple_candidates(generator):
    """Test substitution with multiple valid candidates."""
    text = "el gato negro corre"
    doc = generator.parse_text(text)
    generator.sub_pos_probs = {'NOUN': 0.5, 'ADJ': 0.5}
    np.random.seed(42)
    result = generator._apply_substitution(text, doc)
    # Should modify either noun or adjective
    assert result != text
    assert result.startswith("el") and ("gato" not in result or "negro" not in result) 