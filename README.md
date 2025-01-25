# Spanish Disfluency Generator

A Python tool for generating natural disfluencies in Spanish text. This tool can introduce various types of disfluencies commonly found in spontaneous speech, including:

- Word deletions (DEL)
- Phonological alterations (PHO)
- Word substitutions (SUST)
- Word insertions (INS)
- Word cuts (CUT)
- Word repetitions (REP)
- Filler words (FILL)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/disfluentES.git
cd disfluentES
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the Spanish language model:
```bash
python -m spacy download es_core_news_lg
```

## Usage

The tool can be used from the command line:

```bash
python disfluentes.py --input_text "Tu texto en español" --output_file output.txt --config_file config/default.gin
```

Or with a text file as input:

```bash
python disfluentes.py --input_text input.txt --output_file output.txt
```

### Arguments

- `--input_text`: Input text or path to input file
- `--output_file`: (Optional) Path to output file. If not provided, prints to stdout
- `--config_file`: (Optional) Path to gin config file. Defaults to `config/default.gin`
- `--num_repetitions`: (Optional) Number of disfluencies to apply (overrides config)

## Configuration

- Common Spanish fillers and discourse markers
- Character patterns for phonological changes
- Maximum number of repetitions

You can create custom configurations by copying and modifying the default config file.

# Basic usage
python disfluentes.py --input_text "Tu texto en español"

# Process sentences separately with multiple variations
python disfluentes.py --input_text input.txt --output_file output.txt --process_sentences --num_variations 3

# Apply specific disfluencies in order
python disfluentes.py --input_text "Tu texto" --specific_disfluencies '["DEL", "PHO", "SUST"]'

# Use different level configurations
python disfluentes.py --input_text "Tu texto" --config_file config/levels/primero.gin

# Random disfluencies
python disfluentes.py -i "El gato duerme en la cama" -o output.txt

# Specific disfluency types
python disfluentes.py -i "El gato duerme en la cama" --disfluency_type='["DEL","INS"]'

# Multiple variations
python disfluentes.py -i "El gato duerme. El perro come." --num_variations=3 --process_sentences=True


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
