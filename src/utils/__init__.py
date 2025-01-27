spacy_es_wrong_pos = {
    "casa": {"POS": "NOUN", "Morph": "Gender=Fem|Number=Sing"},
    "elefante": {"POS": "NOUN", "Morph": "Gender=Masc|Number=Sing"},
    "perro": {"POS": "NOUN", "Morph": "Gender=Masc|Number=Sing"},
    "negro": {"POS": "ADJ", "Morph": "Gender=Masc|Number=Sing"},
    "caminaren":{"POS":"ADJ", "Morph": "Gender=Masc|Number=Sing"}
}

default_char_patterns = {
    'substitutions': {
        'consonants': {
            'n': ['d', 'g', 'l', 'r', 't'],
            't': ['d', 'p'],
            'j': ['g', 's'],
            'c': ['s', 'z', 'q'],
            'm': ['n', 'p', 'x'],
            'mp': ['mb', 'p', 'b'],
            'b': ['d', 'p', 'f'],
            'r': ['l', 'n', 'd'],
            'l': ['r', 'n', 'd'],
            'd': ['t', 'b'],
            'p': ['b', 't', 'f'],
            's': ['x', 'd'],
            'v': ['f'],
            'r': ['l', 'n', 'd', 'rr'],
            'ce': ['que']
        },
        'vowels': {
            'i': ['e', 'y'],
            'u': ['e', 'o', 'i'],
            'a': ['i', 'e', 'o'],
            'e': ['a', 'o', 'i', 'ie'],
            'o': ['u', 'a', 'io']
        },
        'diphthongs': {
            'ie': ['e', 'ei'],
            'ue': ['u', 'o', 'e'],
            'ai': ['ae'],
            'ei': ['ie', 'e', 'i'],
            'io': ['i', 'o']
        }
    },
    'insertions': {
        'position': {
            'start': ['p', 'e', 'a', 'c', 'd', 'v'],
            'middle': ['i', 'r', 'u', 'e', 'n', 's'],
            'end': ['n', 's', 'o']
        }
    },
    'deletions': {
        'position': {
            'start': ['a', 'e', 'p'],
            'middle': ['n', 'r', 'p', 'c', 'i', 'e', 'n', 'x', 's'],
            'end': ['s', 'z', 'o', 'a', 'e', 'r']
        }
    }
}