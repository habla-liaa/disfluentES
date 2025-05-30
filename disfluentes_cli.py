#!/usr/bin/env python3
"""Spanish disfluency generator CLI."""

import random
from IPython import embed
import gin
import spacy
from pathlib import Path
from typing import Optional, List, Union
import argparse
from tqdm import tqdm
from transformers.models.whisper.english_normalizer import BasicTextNormalizer
normalizer = BasicTextNormalizer()

from disfluentes.generator import SpanishDisfluencyGenerator

@gin.configurable
def generate_disfluencies(
    input_text: str,
    output_file: Optional[str] = None,
    config_file: Union[str, List[str]] = "config/default.gin",
    recursive_depth: int = 1,
    num_variations: int = 1,
    leave_original_ratio: float = 0.0,
    process_sentences: bool = True,
    normalize_text: bool = True,
    remove_duplicates: bool = False,
    verbose: bool = False

) -> Union[str, List[str]]:
    """Generate disfluencies in Spanish text.
    
    Args:
        input_text: Input text or path to input file
        output_file: Path to output file (optional)
        config_file: Path to gin config file or list of paths that will be merged
        num_variations: Number of variations to generate for each input
        process_sentences: Whether to process text sentence by sentence
        normalize_text: Whether to normalize the text before processing
        remove_duplicates: Whether to remove duplicates
        verbose: Whether to print verbose output
    Returns:
        Text with added disfluencies or list of variations
        
    Examples:
        # Generate random disfluencies using default config
        python disfluentes.py "El gato duerme en la cama" -o output.txt
        
        # Generate specific disfluency types in order
        python disfluentes.py "El gato duerme en la cama" -c config/sustitutions.gin
        
        # Generate multiple variations processing each sentence
        python disfluentes.py "El gato duerme. El perro come." -v 3 -s
        
        # Use a specific configuration level
        python disfluentes.py "El gato duerme" -c config/levels/primero.gin
        
        # Merge multiple config files
        python disfluentes.py "El gato duerme" -c config/base_probs.gin -c config/levels/all.gin
    """

    if len(config_file) == 0:
        config_file = ["config/default.gin"]

    # Load configuration
    if isinstance(config_file, str):
        config_file = [config_file]
    
    # Check if config files exist
    for cfg in config_file:
        if not Path(cfg).is_file():
            raise FileNotFoundError(f"Config file {cfg} not found")

    for cfg in config_file:
        gin.parse_config_file(cfg)
    
    # Read input text
    if Path(input_text).is_file():
        if verbose:
            print("Reading input text from file")
        with open(input_text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input_text
        
    # Initialize generator
    generator = SpanishDisfluencyGenerator(recursive_depth= recursive_depth)
    nlp = spacy.load('es_core_news_lg')
    
    results = []
    if process_sentences:
        # Process each sentence separately
        doc = nlp(text)
        sentences = list(doc.sents)
        for sent in tqdm(sentences, desc="Processing sentences", total=len(sentences),disable=not verbose):            
            if verbose:
                print(sent.text)            
            sent_results = generator.generate_disfluencies(
                    normalizer(sent.text).strip() if normalize_text else sent.text,
                    num_variations, 
                    leave_original_ratio
                )

            results.extend(sent_results)
    else:
        # Process entire text as one unit
        for _ in range(num_variations):
            sent_results = generator.generate_disfluencies(
                normalizer(text).strip() if normalize_text else text,
                num_variations
            )
            results.append(sent_results)
    
    # Remove duplicates and single word results
    results = [result for result in results if len(result.split()) > 1]
    if remove_duplicates:
        results = list(set(results))

    # Write output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, result in enumerate(results, 1):
                f.write(f"{result}\n")
    else:
        return results[0] if len(results) == 1 else results

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Spanish disfluency generator')
    parser.add_argument('input_text', help='Input text or path to input file')
    parser.add_argument('-o', '--output_file', help='Path to output file')
    parser.add_argument('-c', '--config_file', action='append',
                      help='Path to gin config file(s). Can be specified multiple times to merge configs.', default=[])
    parser.add_argument('-r', '--recursive_depth', type=int, default=1,
                      help='Number of disfluencies to apply (overrides config)')
    parser.add_argument('-v', '--num_variations', type=int, default=1,
                      help='Number of variations to generate for each input')
    parser.add_argument('-s', '--process_sentences', action='store_true', default=True,
                      help='Whether to process text sentence by sentence')
    parser.add_argument('-d', '--remove_duplicates', action='store_true', default=False,
                      help='Whether to remove duplicates')
    parser.add_argument('-n', '--normalize_text', action='store_true', default=True,
                      help='Whether to normalize the text before processing')
    parser.add_argument('-l', '--leave_original_ratio', type=float, default=0.0,
                      help='Ratio of original text to leave in the output')
    parser.add_argument('--verbose', action='store_true', default=False,
                      help='Whether to print verbose output')
    return parser.parse_args()

def main():
    """CLI entry point."""
    args = parse_args()
    result = generate_disfluencies(
        input_text=args.input_text,
        output_file=args.output_file,
        config_file=args.config_file,
        recursive_depth=args.recursive_depth,
        num_variations=args.num_variations,
        process_sentences=args.process_sentences,
        normalize_text=args.normalize_text,
        remove_duplicates=args.remove_duplicates,
        leave_original_ratio=args.leave_original_ratio,
        verbose=args.verbose
    )
    if result is not None:
        for res in result:
            print(res)

if __name__ == "__main__":
    main() 