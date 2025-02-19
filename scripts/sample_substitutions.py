#!/usr/bin/env python3

import sys
import os
import gin
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import spacy
import random
from disfluentes.generator import SpanishDisfluencyGenerator

# List of common Spanish words with their POS tags
TEST_WORDS = [
    # Verbs
    ("caminar", "VERB"),
    ("correr", "VERB"), 
    ("escribir", "VERB"),
    ("estudiar", "VERB"),
    ("trabajar", "VERB"),
    # Nouns
    ("gato", "NOUN"),
    ("perro", "NOUN"),
    ("libro", "NOUN"),
    ("mesa", "NOUN"),
    ("casa", "NOUN"),
    # Adjectives
    ("grande", "ADJ"),
    ("pequeño", "ADJ"),
    ("rojo", "ADJ"),
    ("bonito", "ADJ"),
    ("alto", "ADJ"),
    # Determiners
    ("el", "DET"),
    ("la", "DET"),
    ("los", "DET"),
    ("un", "DET"),
    ("una", "DET"),
    # Prepositions
    ("en", "ADP"),
    ("de", "ADP"),
    ("por", "ADP"),
    ("para", "ADP"),
    ("con", "ADP")
]

def parse_args():
    parser = argparse.ArgumentParser(description='Sample substitutions for Spanish words')
    parser.add_argument('--gin_config', type=str, default='config/base_substitution.gin',
                      help='Path to the gin config file')
    parser.add_argument('--seed', type=int, default=42,
                      help='Random seed for reproducibility')
    parser.add_argument('--output', type=str, default='substitution_results.txt',
                      help='Output file path')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Load gin config
    gin.parse_config_file(args.gin_config)
    
    # Initialize generator and set seed for reproducibility
    random.seed(args.seed)
    generator = SpanishDisfluencyGenerator()
    
    # Test each word 3 times with different substitution types
    results = []
    for word, pos in TEST_WORDS:
        results.append(f"\nOriginal word ({pos}): {word}")
        
        # Force only this POS to be modified
        generator.sub_pos_probs = {pos: 1.0}
        
        # Try each substitution type
        for sub_type in ['inflection', 'misspelling']:
            generator.substitution_alteration_subclass = {sub_type: 1.0}
            
            # Generate 3 variations
            for i in range(3):
                doc = generator.parse_text(word)
                result = generator._apply_substitution(doc)
                results.append(f"{sub_type} {i+1}: {result}")
    
    # Write results to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("Substitution Test Results\n")
        f.write("=" * 50 + "\n")
        f.write(f"Config: {args.gin_config}\n")
        f.write(f"Random seed: {args.seed}\n")
        f.write("=" * 50 + "\n\n")
        f.write('\n'.join(results))

if __name__ == "__main__":
    main()
    print("Results have been written to substitution_results.txt") 