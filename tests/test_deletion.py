import pytest
import spacy
import numpy as np
from src.generator import SpanishDisfluencyGenerator

@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()

def test_apply_deletion_with_pos_candidates(generator):
    """Test deletion when there are valid POS candidates."""
    text = "El gato está volando"
    doc = generator.nlp(text)
    generator.del_pos_probs = {'NOUN': 1.0}
    result = generator._apply_deletion(text, doc)
    # With seed 42, should delete "gato" based on POS probabilities
    assert result == "El está volando"

def test_apply_deletion_without_pos_candidates(generator):
    """Test deletion when there are no valid POS candidates."""
    # Using a text where no words match POS tag probabilities
    text = "ah um eh"
    doc = generator.nlp(text)
    result = generator._apply_deletion(text, doc)
    # Should delete a random word since no POS matches
    assert result == "ah eh" or result == "um eh" or result == "ah um"

def test_apply_deletion_single_word(generator):
    """Test deletion with a single word - should return unchanged."""
    text = "gato"
    doc = generator.nlp(text)
    result = generator._apply_deletion(text, doc)
    assert result == text

def test_apply_deletion_empty_text(generator):
    """Test deletion with empty text - should return unchanged."""
    text = ""
    doc = generator.nlp(text)
    result = generator._apply_deletion(text, doc)
    assert result == text

def test_apply_deletion_whitespace(generator):
    """Test deletion with whitespace - should return unchanged."""
    text = "   "
    doc = generator.nlp(text)
    result = generator._apply_deletion(text, doc)
    assert result == text 

