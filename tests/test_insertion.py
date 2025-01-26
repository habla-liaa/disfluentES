import pytest
import numpy as np
from src.generator import SpanishDisfluencyGenerator

@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()

def test_apply_insertion_with_noun(generator):
    """Test article insertion before a noun with gender/number agreement."""
    text = "gato negro"
    doc = generator.parse_text(text)
    # Set probabilities to ensure article insertion before noun
    generator.ins_target_pos = {'NOUN': 1.0, 'PROPN': 1.0}
    generator.ins_type_probs = {'articles': 1.0}
    generator.articles = ['el', 'la', 'los', 'las', 'un', 'una', 'unas', 'unos']
    np.random.seed(42)
    result = generator._apply_insertion(text, doc)
    # With seed 42, should insert "el" before "gato" (masculine singular)
    assert result == "el gato negro" or result == "un gato negro"

def test_apply_insertion_with_feminine_noun(generator):
    """Test article insertion before a feminine noun."""
    text = "casa grande"
    doc = generator.parse_text(text)
    generator.ins_target_pos = {'NOUN': 1.0, 'PROPN': 1.0}
    generator.ins_type_probs = {'articles': 1.0}
    generator.articles = ['el', 'la', 'los', 'las', 'un', 'una', 'unas', 'unos']
    np.random.seed(42)
    result = generator._apply_insertion(text, doc)
    # Should insert feminine article 
    assert result == "la casa grande" or result == "una casa grande"

def test_apply_insertion_preposition(generator):
    """Test preposition insertion."""
    text = "gato negro"
    doc = generator.parse_text(text)
    generator.ins_target_pos = {'NOUN': 1.0}
    generator.ins_type_probs = {'prepositions': 1.0}
    generator.prepositions = ['de']  # Fix preposition for test
    result = generator._apply_insertion(text, doc)
    assert result == "de gato negro"

def test_apply_insertion_conjunction(generator):
    """Test conjunction insertion."""
    text = "gato negro"
    doc = generator.parse_text(text)
    generator.ins_target_pos = {'NOUN': 1.0}
    generator.ins_type_probs = {'conjunctions': 1.0}
    generator.conjunctions = {'CCONJ': ['y'], 'SCONJ': ['que']}  # Fix conjunction for test
    result = generator._apply_insertion(text, doc)
    assert result == "y gato negro" or result == "que gato negro"

def test_apply_insertion_no_candidates(generator):
    """Test insertion when there are no valid candidates."""
    text = "ah eh"  # Interjections without valid POS tags
    doc = generator.parse_text(text)
    result = generator._apply_insertion(text, doc)
    assert result == text

def test_apply_insertion_empty_text(generator):
    """Test insertion with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_insertion(text, doc)
    assert result == text

def test_apply_insertion_whitespace(generator):
    """Test insertion with whitespace."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_insertion(text, doc)
    assert result == text 