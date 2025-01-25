#!/usr/bin/env python3
"""Spanish disfluency generator CLI."""

import fire
import gin
import spacy
from pathlib import Path
from typing import Optional, List, Union
import argparse
import json

from src.generator import SpanishDisfluencyGenerator


@gin.configurable
def generate_disfluencies(
    input_text: str,
    output_file: Optional[str] = None,
    config_file: str = "config/default.gin",
    num_repetitions: int = 1,
    num_variations: int = 1,
    process_sentences: bool = False
) -> Union[str, List[str]]:
    """Generate disfluencies in Spanish text.
    
    Args:
        input_text: Input text or path to input file
        output_file: Path to output file (optional)
        config_file: Path to gin config file
        num_repetitions: Number of disfluencies to apply (overrides config)
        num_variations: Number of variations to generate for each input
        process_sentences: Whether to process text sentence by sentence
        
    Returns:
        Text with added disfluencies or list of variations
        
    Examples:
        # Generate random disfluencies using default config
        python disfluentes.py -i "El gato duerme en la cama" -o output.txt
        
        # Generate specific disfluency types in order
        python disfluentes.py -i "El gato duerme en la cama" --disfluency_type='["DEL","INS"]'
        
        # Generate multiple variations processing each sentence
        python disfluentes.py -i "El gato duerme. El perro come." --num_variations=3 --process_sentences=True
        
        # Use a specific configuration level
        python disfluentes.py -i "El gato duerme" --config_file="config/levels/primero.gin"
    """
    # Load configuration
    gin.parse_config_file(config_file)
    
    # Read input text
    if Path(input_text).is_file():
        with open(input_text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input_text
        
    # Initialize generator
    generator = SpanishDisfluencyGenerator()
    nlp = spacy.load('es_core_news_lg')
    
    results = []
    if process_sentences:
        # Process each sentence separately
        doc = nlp(text)
        for sent in doc.sents:
            sent_variations = []
            for _ in range(num_variations):
                result = generator.generate_disfluencies(
                    sent.text,
                    num_repetitions,
                )
                sent_variations.append(result)
            results.extend(sent_variations)
    else:
        # Process entire text as one unit
        for _ in range(num_variations):
            result = generator.generate_disfluencies(
                text,
                num_repetitions,
            )
            results.append(result)
    
    # Write output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, result in enumerate(results, 1):
                f.write(f"{result}\n")
    else:
        return results[0] if len(results) == 1 else results


def main():
    """CLI entry point."""
    fire.Fire(generate_disfluencies)


if __name__ == "__main__":
    main() 