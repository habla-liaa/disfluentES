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
- **Pre-corrections (PRE)**: A correction to a target word
- **Fillers (FILL)**: Addition of hesitation markers

## Installation 🔧

You can install DisfluentES using any of these methods:

### 1. Install
```bash
pip install git+https://github.com/habla-liaa/disfluentES.git
```

### 2. Download Required Language Model
After installation, download the Spanish language model:
```bash
python -m spacy download es_core_news_lg
```

## Usage ��

### Basic Usage

After installation, you can use the `disfluentes` command directly from your terminal:

```bash
 disfluentes "El gato duerme en la cama" 
```

Outputs:
```
gato duerme en la cama
el gato d duerme en la cama
el el gato duerme en la cama
el gato perdón duerme en la cama
el gato duerme en lo cama
el gato duerme en la ma
el guato duerme en la cama
```


### Advanced Usage

1. **Process Multiple Sentences**:
```bash
disfluentes "El gato duerme. El perro come." \
           --process_sentences \
           --num_variations 3
```

2. **Use Different Difficulty Levels**:
```bash
# Primary level
disfluentes "Tu texto" --config_file config/levels/3grado.gin

# High-school level
disfluentes "Tu texto" --config_file config/levels/1año.gin
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
pytest -v
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation 📚

If you use this tool in your research, please cite:

```bibtex
@software{disfluentES2024,
  author = {Jazmin Vidal, Pablo Riera},
  title = {DisfluentES: A Spanish Disfluency Generator},
  year = {2024},
  url = {https://github.com/habla-liaa/disfluentES}
}
```
