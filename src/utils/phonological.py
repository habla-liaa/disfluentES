"""Phonological operations for Spanish disfluency generation."""

import random
import gin

def do_misspell_word(word: str, char_patterns: dict) -> str:
    """Misspell a word based on phonological patterns."""
    raise NotImplementedError

@gin.configurable
def substitute_char(word: str, char_patterns: dict) -> str:
    """Substitute a character in the word based on phonological patterns."""
    if not word:
        return word
        
    # Choose substitution type
    sub_type = random.choice(list(char_patterns['substitutions'].keys()))
    patterns = char_patterns['substitutions'][sub_type]
    
    if not patterns:
        return word
    
    # Find applicable patterns
    possible_subs = []
    for pattern, replacements in patterns.items():
        if pattern in word:
            possible_subs.append((pattern, replacements))
            
    if not possible_subs:
        return word
        
    # Apply substitution
    pattern, replacements = random.choice(possible_subs)
    replacement = random.choice(replacements)
    return word.replace(pattern, replacement, 1)


@gin.configurable
def insert_char(word: str, char_patterns: dict) -> str:
    """Insert a character in the word based on phonological patterns."""
    if not word:
        return word
        
    # Choose position
    positions = char_patterns['insertions'].get('position', {})
    if not positions:
        return word
    
    position_type = random.choice(list(positions.keys()))
    chars = positions[position_type]
    
    char_to_insert = random.choice(chars)
    
    if position_type == 'start':
        return char_to_insert + word
    elif position_type == 'end':
        return word + char_to_insert
    else:
        pos = random.randint(1, len(word)-1)
        return word[:pos] + char_to_insert + word[pos:]


@gin.configurable
def delete_char(word: str, char_patterns: dict) -> str:
    """Delete a character from the word based on phonological patterns."""
    if not word or len(word) <= 2:
        return word
        
    # Choose position
    positions = char_patterns['deletions'].get('position', {})
    if not positions:
        return word
    
    position_type = random.choice(list(positions.keys()))
    chars = positions[position_type]
    
    # Find applicable deletions
    possible_dels = []
    for char in chars:
        if char in word:
            possible_dels.append(char)
            
    if not possible_dels:
        return word
        
    char_to_delete = random.choice(possible_dels)
    return word.replace(char_to_delete, '', 1) 