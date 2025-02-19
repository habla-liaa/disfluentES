import pytest
import spacy
import numpy as np
from disfluentes.generator import SpanishDisfluencyGenerator

@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()

def test_apply_cut_with_verb(generator):
    """Test cutting a verb."""
    text = "caminando por la calle"
    doc = generator.nlp(text)
    generator.cut_pos_probs = {'VERB': 1.0}
    np.random.seed(42)  # Reset seed for consistent results
    result = generator._apply_cut(doc)
    # Should cut "caminando" to a shorter form
    assert result != text
    assert result.split()[0].startswith("ca") or result.split()[0].endswith("do")
    assert "caminando" not in result

def test_apply_cut_with_noun(generator):
    """Test cutting a noun."""
    text = "el elefante grande"
    doc = generator.parse_text(text)
    generator.cut_pos_probs = {'NOUN': 1.0}
    np.random.seed(42)
    result = generator._apply_cut(doc)
    # Should cut "elefante" to a shorter form
    assert result != text
    assert "elefante" not in result
    assert result.split()[1].startswith("ele") or result.split()[1].endswith("te")

def test_apply_cut_with_adjective(generator):
    """Test cutting an adjective."""
    text = "el coche hermoso"
    doc = generator.parse_text(text)
    generator.cut_pos_probs = {'ADJ': 1.0}
    np.random.seed(42)
    result = generator._apply_cut(doc)
    # Should cut "hermoso" to a shorter form
    assert result != text
    assert "hermoso" not in result
    assert result.split()[2].startswith("her") or result.split()[2].endswith("so")

def test_apply_cut_short_word(generator):
    """Test with a word that's too short to cut."""
    text = "el sol"  # "sol" is 3 letters
    doc = generator.parse_text(text)
    generator.cut_pos_probs = {'NOUN': 1.0}
    result = generator._apply_cut(doc)
    # Should not cut words that are too short
    assert result == text

def test_apply_cut_no_candidates(generator):
    """Test when there are no valid candidates to cut."""
    text = "el y la"  # Only function words
    doc = generator.parse_text(text)
    generator.cut_pos_probs = {'NOUN': 1.0, 'VERB': 1.0, 'ADJ': 1.0}
    result = generator._apply_cut(doc)
    assert result == text

def test_apply_cut_empty_text(generator):
    """Test with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_cut(doc)
    assert result == text

def test_apply_cut_whitespace(generator):
    """Test with whitespace only."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_cut(doc)
    assert result == text


