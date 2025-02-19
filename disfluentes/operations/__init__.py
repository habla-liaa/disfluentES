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


spacy_to_mlconjug3 = {
    ("Fin", "Imp", "Pres", "1", "Plur"): {
        "tense": "Afirmativo",
        "mood": "Imperativo",
        "person": "nosotros",
    },
    ("Fin", "Imp", "Pres", "2", "Sing"): {
        "tense": "Afirmativo",
        "mood": "Imperativo",
        "person": "tú",
    },
    ("Fin", "Imp", "Pres", "2", "Plur"): {
        "tense": "Afirmativo",
        "mood": "Imperativo",
        "person": "ellos",
    },
    ("Fin", "Imp", "Pres", "3", "Plur"): {
        "tense": "Afirmativo",
        "mood": "Imperativo",
        "person": "ellos",
    },
    ("Fin", "Imp", "Pres", "3", "Sing"): {
        "tense": "Afirmativo",
        "mood": "Imperativo",
        "person": "él",
    },
    ("Fin", "Ind", "Fut", "1", "Plur"): {
        "tense": "futuro",
        "mood": "Indicativo",
        "person": "nosotros",
    },
    ("Fin", "Ind", "Fut", "1", "Sing"): {
        "tense": "futuro",
        "mood": "Indicativo",
        "person": "yo",
    },
    ("Fin", "Ind", "Fut", "2", "Sing"): {
        "tense": "futuro",
        "mood": "Indicativo",
        "person": "tú",
    },
    ("Fin", "Ind", "Fut", "3", "Plur"): {
        "tense": "futuro",
        "mood": "Indicativo",
        "person": "ellos",
    },
    ("Fin", "Ind", "Fut", "3", "Sing"): {
        "tense": "futuro",
        "mood": "Indicativo",
        "person": "él",
    },
    ("Fin", "Ind", "Imp", "1", "Plur"): {
        "tense": "pretérito imperfecto",
        "mood": "Indicativo",
        "person": "nosotros",
    },
    ("Fin", "Ind", "Imp", "1", "Sing"): {
        "tense": "pretérito imperfecto",
        "mood": "Indicativo",
        "person": "yo",
    },
    ("Fin", "Ind", "Imp", "2", "Sing"): {
        "tense": "pretérito imperfecto",
        "mood": "Indicativo",
        "person": "tú",
    },
    ("Fin", "Ind", "Imp", "3", "Plur"): {
        "tense": "pretérito imperfecto",
        "mood": "Indicativo",
        "person": "ellos",
    },
    ("Fin", "Ind", "Imp", "3", "Sing"): {
        "tense": "pretérito imperfecto",
        "mood": "Indicativo",
        "person": "él",
    },
    ("Fin", "Ind", "Past", "1", "Plur"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "nosotros",
    },
    ("Fin", "Ind", "Past", "1", "Sing"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "yo",
    },
    ("Fin", "Ind", "Past", "2", "Sing"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "tú",
    },
    ("Fin", "Ind", "Past", "2", "Plur"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "ellos",
    },
    ("Fin", "Ind", "Past", "3", "Plur"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "ellos",
    },
    ("Fin", "Ind", "Past", "3", "Sing"): {
        "tense": "pretérito perfecto simple",
        "mood": "Indicativo",
        "person": "él",
    },
    ("Fin", "Ind", "Pres", "1", "Plur"): {
        "tense": "presente",
        "mood": "Indicativo",
        "person": "nosotros",
    },
    ("Fin", "Ind", "Pres", "1", "Sing"): {
        "tense": "presente",
        "mood": "Indicativo",
        "person": "yo",
    },
    ("Fin", "Ind", "Pres", "2", "Sing"): {
        "tense": "presente",
        "mood": "Indicativo",
        "person": "tú",
    },
    ("Fin", "Ind", "Pres", "3", "Plur"): {
        "tense": "presente",
        "mood": "Indicativo",
        "person": "ellos",
    },
    ("Fin", "Ind", "Pres", "3", "Sing"): {
        "tense": "presente",
        "mood": "Indicativo",
        "person": "él",
    },
    ("Fin", "Sub", "Fut", "1", "Plur"): {
        "tense": "futuro",
        "mood": "Subjuntivo",
        "person": "nosotros",
    },
    ("Fin", "Sub", "Fut", "1", "Sing"): {
        "tense": "futuro",
        "mood": "Subjuntivo",
        "person": "yo",
    },
    ("Fin", "Sub", "Fut", "2", "Plur"): {
        "tense": "futuro",
        "mood": "Subjuntivo",
        "person": "tú",
    },
    ("Fin", "Sub", "Fut", "3", "Plur"): {
        "tense": "futuro",
        "mood": "Subjuntivo",
        "person": "ellos",
    },
    ("Fin", "Sub", "Fut", "3", "Sing"): {
        "tense": "futuro",
        "mood": "Subjuntivo",
        "person": "él",
    },
    ("Fin", "Sub", "Imp", "1", "Plur"): {
        "tense": "pretérito imperfecto 1",
        "mood": "Subjuntivo",
        "person": "nosotros",
    },
    ("Fin", "Sub", "Imp", "1", "Sing"): {
        "tense": "pretérito imperfecto 1",
        "mood": "Subjuntivo",
        "person": "yo",
    },
    ("Fin", "Sub", "Imp", "2", "Sing"): {
        "tense": "pretérito imperfecto 1",
        "mood": "Subjuntivo",
        "person": "tú",
    },
    ("Fin", "Sub", "Imp", "3", "Plur"): {
        "tense": "pretérito imperfecto 1",
        "mood": "Subjuntivo",
        "person": "ellos",
    },
    ("Fin", "Sub", "Imp", "3", "Sing"): {
        "tense": "pretérito imperfecto 1",
        "mood": "Subjuntivo",
        "person": "él",
    },
    ("Fin", "Sub", "Pres", "1", "Plur"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "nosotros",
    },
    ("Fin", "Sub", "Pres", "1", "Sing"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "yo",
    },
    ("Fin", "Sub", "Pres", "2", "Sing"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "tú",
    },
    ("Fin", "Sub", "Pres", "2", "Plural"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "ellos",
    },
    ("Fin", "Sub", "Pres", "3", "Plur"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "ellos",
    },
    ("Fin", "Sub", "Pres", "3", "Sing"): {
        "tense": "presente",
        "mood": "Subjuntivo",
        "person": "él",
    },
}
