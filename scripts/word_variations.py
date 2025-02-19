import spacy
import json
from pathlib import Path
from disfluentes.operations.word_variations import get_word_variations
import fire
# Load spaCy model
nlp = spacy.load("es_core_news_lg")

# read a dir with txt files and get the word variations for each unique word and save in json
def get_word_variations_from_dir(dir_path: Path):
    files = Path(dir_path).glob("*.txt")
    word_variations = {}

    for file in files:
        with open(file, "r") as f:
            words = f.read().split()
        words = list(set(words))
        for word in words:
            word = word.strip() 
                # Example for similarity
            variations = get_word_variations(
                word=word,
                disfluency_type=("similarity", "inflection"),
                nlp=nlp,
                similarity_params={"n_words": 10, "cutoff": 0.8},
            )

            print(f"Similar words for '{word}': {variations}")
            # save in json
            word_variations[word] = variations

    with open("word_variations.json", "w") as f:
        json.dump(word_variations, f)

if __name__ == "__main__":
    fire.Fire(get_word_variations_from_dir)