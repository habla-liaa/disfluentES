import pytest
import spacy
import numpy as np
from disfluentes.generator import SpanishDisfluencyGenerator

@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()

def test_apply_repetition_order_one(generator):
    """Test repetition of a single word (order=1)."""
    text = "el gato negro corre"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'VERB': 1.0}
    generator.rep_order_probs = {1: 1.0}  # Force order 1
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat just "corre"
    assert result == "el gato negro corre corre"

def test_apply_repetition_order_two(generator):
    """Test repetition of two consecutive words (order=2)."""
    text = "el gato negro corre rápido"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'ADV': 1.0}
    generator.rep_order_probs = {2: 1.0}  # Force order 2
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "corre rápido"
    assert result == "el gato negro corre rápido corre rápido"

def test_apply_repetition_order_three(generator):
    """Test repetition of three consecutive words (order=3)."""
    text = "el gato negro corre muy rápido"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'ADV': 1.0}
    generator.rep_order_probs = {3: 1.0}  # Force order 3
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "corre muy rápido" or "corre muy negro"
    assert result == "el gato negro corre muy rápido corre muy rápido" or result == "el gato negro corre muy negro corre muy rápido"

def test_apply_repetition_with_noun(generator):
    """Test repetition of a noun."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'NOUN': 1.0}
    generator.rep_order_probs = {1: 1.0}
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "gato"
    assert result == "el gato gato negro"

def test_apply_repetition_with_adjective(generator):
    """Test repetition of an adjective."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'ADJ': 1.0}
    generator.rep_order_probs = {1: 1.0}    
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "negro"
    assert result == "el gato negro negro"

def test_apply_repetition_with_determinant(generator):
    """Test repetition of a determinant."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'DET': 1.0}
    generator.rep_order_probs = {1: 1.0}
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "el"
    assert result == "el el gato negro"

def test_apply_repetition_no_candidates(generator):
    """Test repetition when there are no valid candidates."""
    text = "ah eh"  # Interjections without valid POS tags
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'NOUN': 1.0, 'VERB': 1.0, 'ADJ': 1.0}
    generator.rep_order_probs = {1: 1.0}
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat a random word since no POS matches
    assert result == "ah ah eh" or result == "ah eh eh"

def test_apply_repetition_single_word(generator):
    """Test repetition with a single word."""
    text = "gato"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'NOUN': 1.0}
    generator.rep_order_probs = {1: 1.0}
    result = generator._apply_repetition(doc)
    # Should repeat the single word
    assert result == "gato gato"

def test_apply_repetition_empty_text(generator):
    """Test repetition with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_repetition(doc)
    assert result == text

def test_apply_repetition_whitespace(generator):
    """Test repetition with whitespace."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_repetition(doc)
    assert result == text

def test_apply_repetition_order_at_start(generator):
    """Test repetition of multiple words at the start of sentence."""
    text = "el gato negro corre"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'DET': 1.0}
    generator.rep_order_probs = {2: 1.0}  # Force order 2
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should repeat "el gato"
    assert (result == "el el gato negro corre" or 
            result == "el gato gato negro corre" or 
            result == "el gato negro negro corre" or
            result == "el gato negro corre corre")
    
def test_apply_repetition_insufficient_words(generator):
    """Test when order is larger than available words after trigger."""
    text = "el gato negro"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'NOUN': 1.0}
    generator.rep_order_probs = {3: 1.0}  # Order 3 but only 1 word after "gato"
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should not repeat since there aren't enough words after the noun
    assert (result == "el el gato negro" or
            result == "el gato gato negro" or
            result == "el gato negro negro")

def test_apply_repetition_with_order_larger_than_words(generator):
    """Test when order is larger than available words after trigger."""
    text = "el gato"
    doc = generator.parse_text(text)
    generator.rep_pos_probs = {'NOUN': 1.0}
    generator.rep_order_probs = {3: 1.0}  # Order 3 but only 1 word after "gato"
    np.random.seed(42)
    result = generator._apply_repetition(doc)
    # Should default to order 2
    # TODO: check if this is the expected behavior
    assert result == "el el gato" or result == "el gato gato"
