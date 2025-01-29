# DisfluentES 🗣️

A Python tool for generating natural disfluencies in Spanish text, simulating spontaneous speech patterns. This tool introduces various types of disfluencies commonly found in natural speech, making text sound more conversational and human-like.

## Features 🌟

### Disfluency Types
- **Deletions (DEL)**: Omission of words (e.g., "El gato duerme" → "gato duerme")
- **Phonological Changes (PHO)**: Sound alterations (e.g., "casa" → "caza")
- **Substitutions (SUB)**: Word replacements with similar meaning or form
  - Inflection changes (gender, number, tense)
  - Similar word substitutions
  - Misspellings
- **Insertions (INS)**: Addition of articles, prepositions, or discourse markers
- **Word Cuts (CUT)**: Partial word pronunciations
- **Repetitions (REP)**: Word repetitions
- **Prefix Alterations (PRE)**: Changes to word beginnings
- **Fillers (FILL)**: Addition of hesitation markers

## Installation 🔧

You can install DisfluentES using any of these methods:

### 1. Install from PyPI (Recommended)
```bash
pip install disfluentES
```

### 2. Install from source
1. Clone the repository:
```bash
git clone https://github.com/habla-liaa/disfluentES.git
cd disfluentES
```

2. Install in development mode:
```bash
pip install -e .
```

### 3. Download Required Language Model
After installation, download the Spanish language model:
```bash
python -m spacy download es_core_news_lg
```

## Usage ��

### Basic Usage

After installation, you can use the `disfluentes` command directly from your terminal:

```bash
disfluentes -i "El gato duerme en la cama" -o output.txt
```

Or if running from source:
```bash
python disfluentes.py -i "El gato duerme en la cama" -o output.txt
```

### Advanced Usage

1. **Process Multiple Sentences**:
```bash
disfluentes -i "El gato duerme. El perro come." \
           --process_sentences \
           --num_variations 3
```

2. **Use Different Difficulty Levels**:
```bash
# Beginner level
disfluentes -i "Tu texto" --config_file config/levels/primero.gin

# Intermediate level
disfluentes -i "Tu texto" --config_file config/levels/tercero.gin

# Advanced level
disfluentes -i "Tu texto" --config_file config/levels/quinto.gin
```

3. **Specify Disfluency Types**:
```bash
disfluentes -i "El gato duerme" \
           --disfluency_type='["DEL","INS"]'
```

### Configuration 🛠️

Available settings include:

- Disfluency type probabilities
- POS tag probabilities for each disfluency type
- Word lists (articles, prepositions, discourse markers)
- Character patterns for phonological changes

Custom configurations can be created by modifying the default config files in the `config/` directory.

### Testing

```bash
python -m pytest tests/test_deletion.py -v
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation 📚

If you use this tool in your research, please cite:

```bibtex
@software{disfluentES2024,
  author = {Your Name},
  title = {DisfluentES: A Spanish Disfluency Generator},
  year = {2024},
  url = {https://github.com/habla-liaa/disfluentES}
}
```

## Acknowledgments 🙏

- SpaCy for their excellent Spanish language model
- The research community for insights on Spanish disfluency patterns
