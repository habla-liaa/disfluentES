import pytest
import spacy
import numpy as np
from src.generator import SpanishDisfluencyGenerator


@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()


def test_apply_precorrection_cut_type(generator):
    """Test precorrection with CUT type."""
    text = "el elefante corre"
    doc = generator.parse_text(text)
    generator.pre_pos_probs = {"NOUN": 1.0}
    generator.pre_type_probs = {"CUT": 1.0}  # Force CUT type
    np.random.seed(42)
    result = generator._apply_precorrection(text, doc)
    # Should insert cut version of "elefante" before it
    print()
    print(result)
    assert "elefante" in result
    assert len(result.split()) == len(text.split()) + 1
    assert (
        result.startswith("el e")
        or result.startswith("el el")
        or result.startswith("el ele")
        or result.startswith("el elef")
        or result.startswith("el elefa")
        or result.startswith("el elefan")
        or result.startswith("el elefant")
    )


def test_apply_precorrection_pre_type(generator):
    """Test precorrection with PRE type."""
    text = "el elefante corre"
    doc = generator.parse_text(text)
    generator.pre_pos_probs = {"NOUN": 1.0}
    generator.pre_type_probs = {"PRE": 1.0}  # Force PRE type
    with pytest.raises(NotImplementedError):
        generator._apply_precorrection(text, doc)


def test_apply_precorrection_no_candidates(generator):
    """Test precorrection when there are no valid candidates."""
    text = "el y la"  # No words longer than 4 characters
    doc = generator.parse_text(text)
    generator.pre_pos_probs = {"NOUN": 1.0, "VERB": 1.0, "ADJ": 1.0}
    generator.pre_type_probs = {"CUT": 1.0}
    result = generator._apply_precorrection(text, doc)
    # Should return unchanged text when no valid candidates
    assert result == text


def test_apply_precorrection_short_word(generator):
    """Test precorrection with words that are too short."""
    text = "el sol brilla"  # "sol" is too short
    doc = generator.parse_text(text)
    generator.pre_pos_probs = {"NOUN": 1.0}
    generator.pre_type_probs = {"CUT": 1.0}
    result = generator._apply_precorrection(text, doc)
    # Should not modify text since "sol" is too short
    assert result == text


def test_apply_precorrection_empty_text(generator):
    """Test precorrection with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_precorrection(text, doc)
    assert result == text


def test_apply_precorrection_whitespace(generator):
    """Test precorrection with whitespace."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_precorrection(text, doc)
    assert result == text


def test_apply_precorrection_multiple_candidates(generator):
    """Test precorrection with multiple valid candidates."""
    text = "el elefante hermoso camina"
    doc = generator.parse_text(text)
    generator.pre_pos_probs = {"NOUN": 0.5, "ADJ": 0.5}
    generator.pre_type_probs = {"CUT": 1.0}
    np.random.seed(42)
    result = generator._apply_precorrection(text, doc)
    # Should insert cut version of either "elefante" or "hermoso"
    assert len(result.split()) == len(text.split()) + 1
    # check 2nd word is in 3th word
    assert (
        result.split()[1] in result.split()[2] or 
        result.split()[2] in result.split()[3]
    )
