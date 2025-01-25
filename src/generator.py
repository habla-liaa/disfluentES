"""Main Spanish disfluency generator module."""

import random
from IPython import embed
import spacy
import gin
from typing import Optional, Dict, List, Union, Set

from .utils import phonological, text_ops


@gin.configurable
class SpanishDisfluencyGenerator:
    """Generator class for Spanish disfluencies."""
    
    def __init__(self, 
                 max_repetitions: int = 3,
                 disfluency_type: List[str] = None,
                 disfluency_type_probs: Dict[str, float] = None,
                 del_pos_probs: Dict[str, float] = None,
                 pho_pos_probs: Dict[str, float] = None,
                 sust_pos_probs: Dict[str, Dict[str, float]] = None,
                 ins_type_probs: Dict[str, float] = None,
                 ins_target_pos: Dict[str, float] = None,
                 cut_pos_probs: Dict[str, float] = None,
                 rep_pos_probs: Dict[str, float] = None,
                 pre_pos_probs: Dict[str, float] = None,
                 articles: List[str] = None,
                 prepositions: List[str] = None,
                 conjunctions: Dict[str, List[str]] = None,
                 discourse_markers: List[str] = None,
                 fillers: List[str] = None,
                 char_patterns: Dict[str, Dict] = None,
                 substitution_alteration_subclass: Dict[str, float] = None):
        """Initialize the generator.
        
        Args:
            max_repetitions: Maximum number of disfluencies to apply
            disfluency_type: Dictionary mapping disfluency types to their probabilities
            del_pos_probs: POS tag probabilities for deletion
            pho_pos_probs: POS tag probabilities for phonological changes
            sust_pos_probs: POS tag and type probabilities for substitution
            ins_type_probs: Probabilities for insertion types
            ins_target_pos: Target POS probabilities for insertion
            cut_pos_probs: POS tag probabilities for cutting
            rep_pos_probs: POS tag probabilities for repetition
            pre_pos_probs: POS tag probabilities for prefix alteration
            articles: List of articles to use for insertions
            prepositions: List of prepositions to use for insertions
            conjunctions: Dictionary mapping conjunction types to lists of conjunctions
            discourse_markers: List of discourse markers to use for insertions
            fillers: List of filler words to use for insertions
            char_patterns: Dictionary of phonological patterns for character operations
            substitution_alteration_subclass: Dictionary mapping substitution types to their probabilities
        """
        try:
            self.nlp = spacy.load('es_core_news_lg')
        except OSError:
            raise OSError("Please install Spanish language model: python -m spacy download es_core_news_lg")
            
        self.max_repetitions = max_repetitions
        self.disfluency_type = disfluency_type or []
        
        # Load disfluency type probabilities from gin config or default values equivalent to all.gin
        self.disfluency_type_probs = disfluency_type_probs or {
            'DEL': 0.069,
            'PHO': 0.035,
            'SUST': 0.267,
            'INS': 0.116,
            'CUT': 0.466,
            'REP': 0.26,
            'PRE': 0.244,
        }
        
        # Load POS probabilities from gin config
        self.del_pos_probs = del_pos_probs or {}
        self.pho_pos_probs = pho_pos_probs or {}
        self.sust_pos_probs = sust_pos_probs or {}
        self.ins_type_probs = ins_type_probs or {}
        self.ins_target_pos = ins_target_pos or {}
        self.cut_pos_probs = cut_pos_probs or {}
        self.rep_pos_probs = rep_pos_probs or {}
        self.pre_pos_probs = pre_pos_probs or {}
        
        # Load substitution alteration subclass probabilities
        self.substitution_alteration_subclass = substitution_alteration_subclass or {
            'misspelling': 0.3,
            'inflection': 0.5,
            'similarity': 0.2
        }
        
        # Load word lists and patterns from gin config
        self.articles = articles or []
        self.prepositions = prepositions or []
        self.conjunctions = conjunctions or {}
        self.discourse_markers = discourse_markers or []
        self.fillers = fillers or []
        self.char_patterns = char_patterns or {
            'substitutions': {
                'consonants': {'b': ['v'], 'v': ['b'], 's': ['z'], 'z': ['s']},
                'vowels': {'e': ['i'], 'i': ['e'], 'o': ['u'], 'u': ['o']},
                'diphthongs': {'ie': ['ei'], 'ei': ['ie'], 'ue': ['eu'], 'eu': ['ue']}
            },
            'insertions': {
                'position': {
                    'start': ['e', 'a'],
                    'middle': ['s', 'n', 'r'],
                    'end': ['s', 'n', 'r']
                }
            },
            'deletions': {
                'position': {
                    'start': ['e', 'a', 'h'],
                    'middle': ['s', 'n', 'r'],
                    'end': ['s', 'n', 'r']
                }
            }
        }
        
    def generate_disfluencies(self, 
                            text: str, 
                            num_repetitions: Optional[int] = None) -> str:
        """Generate disfluencies in the input text.
        
        Args:
            text: Input text to add disfluencies to
            num_repetitions: Number of disfluencies to apply (defaults to max_repetitions)
            disfluency_type: List of specific disfluency types to apply in order.
                           Available types: ['DEL', 'PHO', 'SUST', 'INS', 'CUT', 'REP', 'PRE', 'FILL']
            disfluency_type_probs: List of specific disfluency types to apply in order.

        Returns:
            Text with added disfluencies
        """
        if not text:
            return text
            
        num_repetitions = num_repetitions or self.max_repetitions
        doc = self.nlp(text)
        
        result = text
        if self.disfluency_type:
            # Deterministic mode: apply specified disfluencies in order
            for disfluency in self.disfluency_type:
                result = self._apply_disfluency(disfluency, result, doc)
                doc = self.nlp(result)
        else:
            # Random mode: choose disfluencies based on probabilities
            for _ in range(num_repetitions):
                disfluency = random.choices(
                    list(self.disfluency_type_probs.keys()),
                    weights=list(self.disfluency_type_probs.values())
                )[0]
                result = self._apply_disfluency(disfluency, result, doc)
                doc = self.nlp(result)
                
        return result
        
    def _apply_disfluency(self, disfluency: str, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply a specific disfluency type."""
        if disfluency == 'DEL':
            return self._apply_deletion(text, doc)
        elif disfluency == 'PHO':
            return self._apply_phonological(text, doc)
        elif disfluency == 'SUST':
            return self._apply_substitution(text, doc)
        elif disfluency == 'INS':
            return self._apply_insertion(text, doc)
        elif disfluency == 'CUT':
            return self._apply_cut(text, doc)
        elif disfluency == 'REP':
            return self._apply_repetition(text, doc)
        elif disfluency == 'PRE':
            return self._apply_precorrection(text, doc)
        elif disfluency == 'FILL':
            return self._apply_filler(text)
        return text
        
    def _apply_deletion(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word deletion disfluency."""

        # If only one word, return text
        if len(text.split()) == 1:
            return text
        
        # If empty text, return text
        if len(text.strip()) == 0:
            return text

        # Select words based on POS tag probabilities
        candidates = [(i, token) for i, token in enumerate(doc) 
                     if token.pos_ in self.del_pos_probs]
        
        if not candidates: # delete a random word
            words = text.split()
            words.pop(random.randint(0, len(words) - 1))
            return ' '.join(words)
            
        # Weight by POS probability
        weights = [self.del_pos_probs[token.pos_] for _, token in candidates]
        idx, _ = random.choices(candidates, weights=weights)[0]
        
        words = text.split()
        words.pop(idx)
        return ' '.join(words)
        
    def _apply_phonological(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply phonological disfluency."""
        
        # Select content words based on POS probabilities
        candidates = [(i, token) for i, token in enumerate(doc) 
                     if token.pos_ in self.pho_pos_probs]
        
        weights = [self.pho_pos_probs[token.pos_] for _, token in candidates]
        
        if not candidates:
            candidates = [(i, token) for i, token in enumerate(doc)]
            weights = [1.0] * len(candidates)

        # Weight by POS probability
        idx, token = random.choices(candidates, weights=weights)[0]
        words = text.split()
        
        # Apply random phonological operation
        op = random.choice([
            lambda x: phonological.substitute_char(x, self.char_patterns),
            lambda x: phonological.insert_char(x, self.char_patterns),
            lambda x: phonological.delete_char(x, self.char_patterns)
        ])        

        words[idx] = op(token.text)
        return ' '.join(words)
    
    def _apply_substitution(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word substitution disfluency. Ensures at least one substitution occurs."""
        original_text = text
        max_attempts = 3
        
        for _ in range(max_attempts):
            candidates = [(i, token) for i, token in enumerate(doc) if token.pos_ in self.sust_pos_probs and (token.has_vector or token.pos_ in ['DET', 'ADP'])]
            if not candidates:
                candidates = [(i, token) for i, token in enumerate(doc)]
            
            idx, token = random.choice(candidates)
            words = text.split()
            
            sub_type = random.choices(list(self.substitution_alteration_subclass.keys()),
                                    weights=list(self.substitution_alteration_subclass.values()))[0]
            if not isinstance(token, spacy.tokens.Token):
                continue

            if token.pos_ in ['VERB', 'AUX']:
                if sub_type == 'inflection' and token.morph: 
                    try: 
                        if token.morph.get('VerbForm') == ['Fin']:
                            number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                            inflected = token._.inflect({'Number': number})
                            if inflected:
                                words[idx] = inflected
                        else:
                            inflected = token.lemma_ if token.text != token.lemma_ else token._.inflect('VerbForm=Fin')
                            if inflected:
                                words[idx] = inflected
                    except: 
                        continue
                elif sub_type == 'similarity' and token.has_vector and token.vector_norm > 0:
                    similar_words = []
                    for lex in token.doc.vocab:
                        if (lex.has_vector and lex.vector_norm > 0 and lex.cluster == token.cluster and  # Use cluster ID to filter similar words
                        token.similarity(lex) > 0.5):
                            similar_words.append(lex.text)

                    if similar_words:
                        words[idx] = random.choice(similar_words)
                else:  # misspelling
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
                
            elif token.pos_ in ['NOUN', 'ADJ']:
                if sub_type == 'inflection' and token.morph:
                    try:
                        change_type = random.choice(['number', 'gender'])
                        if change_type == 'number':
                            number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                            inflected = token._.inflect({'Number': number})
                            if inflected:
                                words[idx] = inflected
                        else:
                            gender = 'Fem' if 'Masc' in token.morph.get('Gender', []) else 'Masc'
                            inflected = token._.inflect({'Gender': gender})
                            if inflected:
                                words[idx] = inflected
                    except:
                        continue
                elif sub_type == 'similarity' and token.has_vector and token.vector_norm > 0:
                    similar_words = []

                    for lex in token.doc.vocab:
                        if (lex.has_vector and lex.vector_norm > 0 and lex.cluster == token.cluster and  # Use cluster ID to filter similar words
                        token.similarity(lex) > 0.5):
                            similar_words.append(lex.text)
                    if similar_words:
                        words[idx] = random.choice(similar_words)
                else:
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
                
            elif token.pos_ == 'DET':
                det_map = {
                    'la': 'una', 'una': 'la',
                    'el': 'un', 'un': 'el',
                    'los': 'unos', 'unos': 'los',
                    'las': 'unas', 'unas': 'las'
                }
                if token.text.lower() in det_map:
                    words[idx] = det_map[token.text.lower()]
                else:
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)   
            elif token.pos_ == 'ADP':
                prepositions = ['de', 'en', 'a', 'por', 'para', 'con', 'sin']
                if token.text in prepositions:
                    available_preps = [p for p in prepositions if p != token.text]
                    words[idx] = random.choice(available_preps)
                else:
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            result = ' '.join(words)
            if result != original_text:
                return result



    '''
    def _apply_substitution(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word substitution disfluency."""
        # Get candidates based on POS
        candidates = [(i, token) for i, token in enumerate(doc) 
                     if token.pos_ in self.sust_pos_probs]
        
        if not candidates:
            candidates = [(i, token) for i, token in enumerate(doc)]
        
        
        idx, token = random.choice(candidates)
        words = text.split()

        # if token pos is not in sust_pos_probs, return phonological error
        if token.pos_ not in self.sust_pos_probs:
            words[idx] = phonological.substitute_char(token.text, self.char_patterns)
        
        # Get substitution type probabilities for this POS
        sub_type = random.choices(list(self.substitution_alteration_subclass.keys()),
                                    weights=list(self.substitution_alteration_subclass.values()))[0]
        
        # Apply substitution based on type and POS
        if token.pos_ in ['VERB', 'AUX']:
            if sub_type == 'inflection':
                # Change verb number or tense
                try:
                    if token.morph.get('VerbForm') == ['Fin']:
                        number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                        inflected = token._.inflect({'Number': number})
                        if inflected:
                            words[idx] = inflected
                    else:
                        inflected = token.lemma_ if token.text != token.lemma_ else token._.inflect('VerbForm=Fin')
                        if inflected:
                            words[idx] = inflected
                except:
                    # Fallback to misspelling
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            
            elif sub_type == 'similarity':
                # Use vector similarity for similar verbs
                if token.has_vector and token.vector_norm > 0:
                    similar_words = []
                    for word in token.vocab:
                        if word.has_vector and word.vector_norm > 0 and word.pos_ == token.pos_:
                            similarity = token.similarity(word)
                            if similarity > 0.5 and similarity < 1.0:
                                similar_words.append(word.text)
                    if similar_words:
                        words[idx] = random.choice(similar_words)
                else:
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            else:  # misspelling
                words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            
        elif token.pos_ in ['NOUN', 'ADJ']:
            if sub_type == 'inflection':
                try:
                    # Randomly choose between number and gender changes
                    change_type = random.choice(['number', 'gender'])
                    if change_type == 'number':
                        number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                        inflected = token._.inflect({'Number': number})
                        if inflected:
                            words[idx] = inflected
                    else:  # gender
                        gender = 'Fem' if 'Masc' in token.morph.get('Gender', []) else 'Masc'
                        inflected = token._.inflect({'Gender': gender})
                        if inflected:
                            words[idx] = inflected
                except:
                    # Fallback to simple gender changes
                    word = token.text
                    if word.endswith('o'): 
                        words[idx] = word[:-1] + 'a'
                    elif word.endswith('a'): 
                        words[idx] = word[:-1] + 'o'
            elif sub_type == 'similarity':
                # Use vector similarity for similar nouns/adjectives
                
                
                if token.has_vector and token.vector_norm > 0:
                    similar_words = []
                    for word in token.vocab:
                        embed()
                        if word.has_vector and word.vector_norm > 0 and word.pos_ == token.pos_:
                            similarity = token.similarity(word)
                            if similarity > 0.5 and similarity < 1.0:
                                similar_words.append(word.text)
                    if similar_words:
                        words[idx] = random.choice(similar_words)
               
                else:
                    words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            else:  # misspelling
                words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            
        elif token.pos_ == 'DET':
            # Map between definite and indefinite articles
            det_map = {
                'la': 'una', 'una': 'la',
                'el': 'un', 'un': 'el',
                'los': 'unos', 'unos': 'los',
                'las': 'unas', 'unas': 'las'
            }
            if token.text.lower() in det_map:
                words[idx] = det_map[token.text.lower()]
            else:
                words[idx] = phonological.substitute_char(token.text, self.char_patterns)
            
        elif token.pos_ == 'ADP':
            # Substitute prepositions
            prepositions = ['de', 'en', 'a', 'por', 'para', 'con', 'sin']
            if token.text in prepositions:
                available_preps = [p for p in prepositions if p != token.text]
                words[idx] = random.choice(available_preps)
            else:
                words[idx] = phonological.substitute_char(token.text, self.char_patterns)
        else:
            words[idx] = phonological.substitute_char(token.text, self.char_patterns)
                
        return ' '.join(words)
    '''
    def _apply_insertion(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word insertion disfluency."""
        words = text.split()
        
        # Select insertion position based on target POS
        candidates = [(i, token.pos_, token) for i, token in enumerate(doc)
                     if token.pos_ in self.ins_target_pos]
                     
        if not candidates:
            return text
            
        # Weight by POS probability
        weights = [self.ins_target_pos[pos] for _, pos, _ in candidates]
        target_idx, _, target_token = random.choices(candidates, weights=weights)[0]
        
        # Choose insertion type based on probabilities
        word_type = random.choices(
            list(self.ins_type_probs.keys()),
            weights=list(self.ins_type_probs.values())
        )[0]
        
        # Insert appropriate word based on type and context
        if word_type == 'articles' and target_token.pos_ in ['NOUN', 'ADJ']:
            gender = target_token.morph.get('Gender', [''])[0]
            number = target_token.morph.get('Number', [''])[0]                   

            if gender == 'fem' and number == 'sing':
                insert_word = random.choice(['la', 'una'])
            elif gender == 'fem' and number == 'plur':
                insert_word = random.choice(['las', 'unas'])
            elif gender == 'masc' and number == 'sing':
                insert_word = random.choice(['el', 'un'])
            elif gender == 'masc' and number == 'plur':
                insert_word = random.choice(['los', 'unos'])
            else:
                insert_word = random.choice(self.articles)
        elif word_type == 'prepositions':
            insert_word = random.choice(self.prepositions)
        elif word_type == 'conjunctions':
            # Choose between coordinating and subordinating conjunctions
            conj_type = random.choice(['CCONJ', 'SCONJ'])
            insert_word = random.choice(self.conjunctions[conj_type])
        else: # discourse_markers
            # TODO: Add discourse markers after any a PRE disfluency instead of regular insertion
            insert_word = random.choice(self.discourse_markers)
                
        words.insert(target_idx, insert_word)
        return ' '.join(words)
        
    def _apply_cut(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word cutting disfluency."""
        candidates = [(i, token) for i, token in enumerate(doc) 
                     if token.pos_ in self.cut_pos_probs and len(token.text) > 3]
        
        if not candidates:
            return text
            
        # Weight by POS probability
        weights = [self.cut_pos_probs[token.pos_] for _, token in candidates]
        idx, token = random.choices(candidates, weights=weights)[0]
        
        words = text.split()
        words[idx] = text_ops.cut_word(token.text)
        return ' '.join(words)
        
    def _apply_repetition(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply word repetition disfluency."""
        candidates = [(i, token) for i, token in enumerate(doc)
                     if token.pos_ in self.rep_pos_probs]
                     
        if not candidates:
            return text
            
        # Weight by POS probability
        weights = [self.rep_pos_probs[token.pos_] for _, token in candidates]
        result, success = text_ops.repeat_word(text, dict(zip(
            [token.pos_ for _, token in candidates],
            weights
        )))
        return result if success else text
        
    def _apply_precorrection(self, text: str, doc: spacy.tokens.Doc) -> str:
        """Apply precorrection disfluency."""
        candidates = [(i, token) for i, token in enumerate(doc)
                     if token.pos_ in self.pre_pos_probs and len(token.text) > 4]
                     
        if not candidates:
            return text
            
        # Weight by POS probability
        weights = [self.pre_pos_probs[token.pos_] for _, token in candidates]
        idx, token = random.choices(candidates, weights=weights)[0]
        
        words = text.split()
        # Alter the prefix (first 2-3 characters)
        prefix_len = random.randint(2, 3)
        if len(token.text) > prefix_len:
            words[idx] = phonological.substitute_char(token.text[:prefix_len], self.char_patterns) + token.text[prefix_len:]
            
        return ' '.join(words)
        
    def _apply_filler(self, text: str) -> str:
        """Apply filler word insertion disfluency."""
        if not text:
            return text
            
        words = text.split()
        if not words:
            return text
            
        # Choose a random filler word
        filler = random.choice(self.fillers)
        
        # Insert at a random position
        insert_pos = random.randint(0, len(words))
        words.insert(insert_pos, filler)
        
        return ' '.join(words) 