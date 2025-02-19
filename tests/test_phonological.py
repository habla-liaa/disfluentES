import pytest
import spacy
import numpy as np
from disfluentes.generator import SpanishDisfluencyGenerator


@pytest.fixture
def generator():
    """Create a SpanishDisfluencyGenerator instance for testing."""
    np.random.seed(42)  # Set random seed for reproducibility
    return SpanishDisfluencyGenerator()


def test_apply_phonological_consonant(generator):
    """Test consonant substitution in a word."""
    text = "perro negro"
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0}
    generator.char_patterns = {
        "substitutions": {"consonants": {"rr": ["r"]}},
        "insertions": {"position": {"start": ["e"]}},
        "deletions": {"position": {"start": ["p"]}},
    }
    np.random.seed(42)  # Reset seed for consistent results
    result = generator._apply_phonological(doc)
    # Should substitute 'rr' with 'r' in 'perro'
    assert result == "pero negro" or result == "eperro negro" or result == "erro negro"


def test_apply_phonological_vowel_substitution(generator):
    """Test vowel substitution in a word."""
    text = "mesa verde"
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0}
    generator.char_patterns = {
        "substitutions": {
            "vowels": {"e": ["i"]},
        }
    }
    np.random.seed(42)
    result = generator._apply_phonological(doc)
    # Should substitute 'e' with 'i' in 'mesa'
    assert result == "misa verde"


def test_apply_phonological_char_insertion(generator):
    """Test character insertion in a word."""
    text = "casa roja"
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0}
    generator.char_patterns = {
        "insertions": {
            "position": {
                "start": ["e"],
            }
        },
    }
    np.random.seed(42)
    result = generator._apply_phonological(doc)
    # Should insert 'e' at the start of 'casa'
    assert result == "ecasa roja"


def test_apply_phonological_char_deletion(generator):
    """Test character deletion in a word."""
    text = "mascara azul"
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0}
    generator.char_patterns = {"deletions": {"position": {"middle": ["s"]}}}
    np.random.seed(42)
    result = generator._apply_phonological(doc)
    # Should delete one 'r' from 'carro'
    assert result == "macara azul"


def test_apply_phonological_diphthong_substitution(generator):
    """Test diphthong substitution in a word."""
    text = "cielo azul"
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0}
    generator.char_patterns = {
        "substitutions": {"diphthongs": {"ie": ["e"]}},
    }
    np.random.seed(42)
    result = generator._apply_phonological(doc)
    # Should substitute 'ie' with 'e' in 'cielo'
    assert result == "celo azul"


def test_apply_phonological_no_candidates(generator):
    """Test when there are no valid candidates for phonological changes."""
    text = "y o"  # Only function words
    doc = generator.parse_text(text)
    generator.pho_pos_probs = {"NOUN": 1.0, "VERB": 1.0, "ADJ": 1.0}
    result = generator._apply_phonological(doc)
    # Should return unchanged text when no valid candidates
    assert result == text


def test_apply_phonological_empty_text(generator):
    """Test with empty text."""
    text = ""
    doc = generator.parse_text(text)
    result = generator._apply_phonological(doc)
    assert result == text


def test_apply_phonological_whitespace(generator):
    """Test with whitespace only."""
    text = "   "
    doc = generator.parse_text(text)
    result = generator._apply_phonological(doc)
    assert result == text
