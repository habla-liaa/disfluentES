"""Main Spanish disfluency generator module."""

import random
from IPython import embed
import spacy
import gin
from typing import Optional, Dict, List, Union, Set
from .operations import phonological, spacy_es_wrong_pos, default_char_patterns
from .operations import text as text_ops
from spacy_syllables import SpacySyllables


@gin.configurable
class SpanishDisfluencyGenerator:
    """Generator class for Spanish disfluencies."""

    def __init__(
        self,
        max_repetitions: int = 3,
        disfluency_type: List[str] = None,
        disfluency_type_probs: Dict[str, float] = None,
        del_pos_probs: Dict[str, float] = None,
        pho_pos_probs: Dict[str, float] = None,
        sub_pos_probs: Dict[str, Dict[str, float]] = None,
        sub_type_probs: Dict[str, Dict[str, float]] = None,
        adj_inflection_probs: Dict[str, float] = None,
        verb_conjugation_probs: Dict[str, float] = None,
        articles_map: Dict[str, List[str]] = None,
        ins_type_probs: Dict[str, float] = None,
        ins_target_pos: Dict[str, float] = None,
        cut_pos_probs: Dict[str, float] = None,
        rep_pos_probs: Dict[str, float] = None,
        rep_order_probs: Dict[int, float] = None,
        pre_pos_probs: Dict[str, float] = None,
        pre_type_probs: Dict[str, float] = None,
        substitution_similarity_params: Dict[str, float] = None,
        articles: List[str] = None,
        prepositions: List[str] = None,
        conjunctions: Dict[str, List[str]] = None,
        discourse_markers: List[str] = None,
        fillers: List[str] = None,
        char_patterns: Dict[str, Dict] = None,
    ):
        """Initialize the generator.

        Args:
            max_repetitions: Maximum number of disfluencies to apply
            disfluency_type: Dictionary mapping disfluency types to their probabilities
            del_pos_probs: POS tag probabilities for deletion
            pho_pos_probs: POS tag probabilities for phonological changes
            sub_pos_probs: POS tag and type probabilities for substitution
            sub_type_probs: Substitution type probabilities
            adj_inflection_probs: Probabilities for noun inflection
            verb_conjugation_probs: Probabilities for verb conjugation
            ins_type_probs: Probabilities for insertion types
            ins_target_pos: Target POS probabilities for insertion
            cut_pos_probs: POS tag probabilities for cutting
            rep_pos_probs: POS tag probabilities for repetition
            rep_order_probs: Probabilities for repetition order
            pre_pos_probs: POS tag probabilities for prefix alteration
            pre_type_probs: Probabilities for prefix alteration type
            substitution_similarity_params: Parameters for substitution similarity
            articles: List of articles to use for insertions
            prepositions: List of prepositions to use for insertions
            conjunctions: Dictionary mapping conjunction types to lists of conjunctions
            discourse_markers: List of discourse markers to use for insertions
            fillers: List of filler words to use for insertions
            char_patterns: Dictionary of phonological patterns for character operations
        """
        try:
            self.nlp = spacy.load("es_core_news_lg")
            self.nlp.add_pipe("syllables", after="ner")
        except OSError:
            raise OSError(
                "Please install Spanish language model: python -m spacy download es_core_news_lg"
            )

        self.max_repetitions = max_repetitions
        self.disfluency_type = disfluency_type

        # Load disfluency type probabilities from gin config or default values equivalent to all.gin
        self.disfluency_type_probs = disfluency_type_probs

        # Load POS probabilities from gin config
        self.del_pos_probs = del_pos_probs
        self.pho_pos_probs = pho_pos_probs
        self.sub_pos_probs = sub_pos_probs
        self.sub_type_probs = sub_type_probs
        self.adj_inflection_probs = adj_inflection_probs
        self.verb_conjugation_probs = verb_conjugation_probs
        self.ins_type_probs = ins_type_probs
        self.ins_target_pos = ins_target_pos
        self.cut_pos_probs = cut_pos_probs
        self.rep_pos_probs = rep_pos_probs
        self.rep_order_probs = rep_order_probs
        self.pre_pos_probs = pre_pos_probs
        self.pre_type_probs = pre_type_probs

        # Load substitution similarity parameters
        self.substitution_similarity_params = substitution_similarity_params

        # Load word lists and patterns from gin config
        self.articles = articles
        self.prepositions = prepositions
        self.conjunctions = conjunctions
        self.discourse_markers = discourse_markers
        self.fillers = fillers
        self.char_patterns = char_patterns or default_char_patterns
        self.articles_map = articles_map

    def parse_text(self, text: str) -> spacy.tokens.Doc:
        """Parse the input text into a spacy Doc object."""
        doc = self.nlp(text)
        for token in doc:
            if token.text in spacy_es_wrong_pos:
                token.pos_ = spacy_es_wrong_pos[token.text]["POS"]
                token.set_morph(spacy_es_wrong_pos[token.text]["Morph"])
        return doc

    def generate_disfluencies(
        self, text: str, num_repetitions: Optional[int] = None
    ) -> str:
        """Generate disfluencies in the input text.

        Args:
            text: Input text to add disfluencies to
            num_repetitions: Number of disfluencies to apply (defaults to max_repetitions)
            disfluency_type: List of specific disfluency types to apply in order.
                           Available types: ['DEL', 'PHO', 'SUB', 'INS', 'CUT', 'REP', 'PRE', 'FILL']
            disfluency_type_probs: List of specific disfluency types to apply in order.

        Returns:
            Text with added disfluencies
        """
        if not text:
            return text

        num_repetitions = num_repetitions or self.max_repetitions

        doc = self.parse_text(text)

        if self.disfluency_type:
            # Deterministic mode: apply specified disfluencies in order
            for disfluency in self.disfluency_type:
                result_text = self._apply_disfluency(disfluency, doc)
                doc = self.nlp(result_text)
        else:
            # Random mode: choose disfluencies based on probabilities
            for _ in range(num_repetitions):
                disfluency = random.choices(
                    list(self.disfluency_type_probs.keys()),
                    weights=list(self.disfluency_type_probs.values()),
                )[0]
                not_failed = True
                while not_failed:
                    try:    
                        result_text = self._apply_disfluency(disfluency, doc)
                        doc = self.nlp(result_text)
                        not_failed = False
                    except:
                        print("Disfluency failed for", disfluency, doc.text)
                        pass

        return result_text

    def _apply_disfluency(self, disfluency: str, doc: spacy.tokens.Doc) -> str:
        """Apply a specific disfluency type."""
        if disfluency == "DEL":
            return self._apply_deletion(doc)
        elif disfluency == "PHO":
            return self._apply_phonological(doc)
        elif disfluency == "SUB":
            return self._apply_substitution(doc)
        elif disfluency == "INS":
            return self._apply_insertion(doc)
        elif disfluency == "CUT":
            return self._apply_cut(doc)
        elif disfluency == "REP":
            return self._apply_repetition(doc)
        elif disfluency == "PRE":
            return self._apply_precorrection(doc)
        elif disfluency == "FILL":
            return self._apply_filler(doc)
        else:
            raise ValueError(f"Invalid disfluency type: {disfluency}")

    def _apply_deletion(self, doc: spacy.tokens.Doc) -> str:
        """Apply word deletion disfluency."""

        text = doc.text
        # If only one word, return text
        if len(text.split()) == 1:
            return text

        # If empty text, return text
        if len(text.strip()) == 0:
            return text

        # Select words based on POS tag probabilities
        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.del_pos_probs
        ]

        if not candidates:  # delete a random word
            words = text.split()
            words.pop(random.randint(0, len(words) - 1))
            return " ".join(words)

        # Weight by POS probability
        weights = [self.del_pos_probs[token.pos_] for _, token in candidates]
        idx, _ = random.choices(candidates, weights=weights)[0]

        words = text.split()
        words.pop(idx)
        return " ".join(words)

    def _apply_phonological(self, doc: spacy.tokens.Doc) -> str:
        """Apply phonological disfluency."""

        text = doc.text
        if len(text.strip()) == 0:
            return text

        # Select content words based on POS probabilities
        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.pho_pos_probs
        ]

        weights = [self.pho_pos_probs[token.pos_] for _, token in candidates]

        if not candidates:
            candidates = [(i, token) for i, token in enumerate(doc)]
            weights = [1.0] * len(candidates)

        # Weight by POS probability
        idx, token = random.choices(candidates, weights=weights)[0]
        words = text.split()

        # Apply random phonological operation
        ops = []
        if "substitutions" in self.char_patterns:
            ops.append(lambda x: phonological.substitute_char(x, self.char_patterns))
        if "insertions" in self.char_patterns:
            ops.append(lambda x: phonological.insert_char(x, self.char_patterns))
        if "deletions" in self.char_patterns:
            ops.append(lambda x: phonological.delete_char(x, self.char_patterns))
        op = random.choice(ops)

        words[idx] = op(token.text)
        return " ".join(words)

    def _apply_substitution(self, doc: spacy.tokens.Doc) -> str:
        """Apply word substitution disfluency. Ensures at least one substitution occurs."""

        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.sub_pos_probs and token.pos_ in self.sub_type_probs
        ]
        if not candidates:
            candidates = [(i, token) for i, token in enumerate(doc)]

        text = doc.text
        words = text.split()

        weights = [self.sub_pos_probs[token.pos_] for _, token in candidates]

        idx, token = random.choices(candidates, weights=weights)[0]

        sub_type = random.choices(
            list(self.sub_type_probs[token.pos_].keys()),
            weights=list(self.sub_type_probs[token.pos_].values()),
        )[0]

        try:
            words[idx] = text_ops.do_substitution(
                token,
                sub_type,
                self.nlp,
                self.adj_inflection_probs,
                self.verb_conjugation_probs,
            self.substitution_similarity_params,
                self.char_patterns,
                self.articles_map,
                self.prepositions,
                self.conjunctions,
            )
        except:
            print("Substitution failed for", token)
            pass

        # if  there is a None in the list print sub_type
        if None in words:
            print(sub_type, token.pos_, token.text)
            embed()

        result = " ".join(words)

        

        return result

    def _apply_insertion(self, doc: spacy.tokens.Doc) -> str:
        """Apply word insertion disfluency."""

        if len(doc.text.strip()) == 0:
            return doc.text

        text = doc.text
        words = text.split()
        # Select insertion position based on target POS
        candidates = [
            (i, token.pos_, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.ins_target_pos
        ]

        if not candidates:
            return text

        # Weight by POS probability
        weights = [self.ins_target_pos[pos] for _, pos, _ in candidates]
        target_idx, _, target_token = random.choices(candidates, weights=weights)[0]

        # Choose insertion type based on probabilities
        word_type = random.choices(
            list(self.ins_type_probs.keys()), weights=list(self.ins_type_probs.values())
        )[0]

        # Insert appropriate word based on type and context
        if word_type == "articles" and target_token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            gender = target_token.morph.get("Gender", [""])[0]
            number = target_token.morph.get("Number", [""])[0]

            if gender == "Fem" and number == "Sing":
                insert_word = random.choice(["la", "una"])
            elif gender == "Fem" and number == "Plur":
                insert_word = random.choice(["las", "unas"])
            elif gender == "Masc" and number == "Sing":
                insert_word = random.choice(["el", "un"])
            elif gender == "Masc" and number == "Plur":
                insert_word = random.choice(["los", "unos"])
            else:
                insert_word = random.choice(self.articles)
        elif word_type == "prepositions":
            insert_word = random.choice(self.prepositions)
        elif word_type == "conjunctions":
            # Choose between coordinating and subordinating conjunctions
            conj_type = random.choice(["CCONJ", "SCONJ"])
            insert_word = random.choice(self.conjunctions[conj_type])
        else:  # discourse_markers
            # TODO: Add discourse markers after any a PRE disfluency instead of regular insertion
            insert_word = random.choice(self.discourse_markers)

        words.insert(target_idx, insert_word)
        return " ".join(words)

    def _apply_cut(self, doc: spacy.tokens.Doc) -> str:
        """Apply word cutting disfluency."""
        text = doc.text

        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.cut_pos_probs and len(token.text) > 3
        ]

        if not candidates:
            return text

        # Weight by POS probability
        weights = [self.cut_pos_probs[token.pos_] for _, token in candidates]
        idx, token = random.choices(candidates, weights=weights)[0]

        words = text.split()
        words[idx] = text_ops.cut_word(token)
        return " ".join(words)

    def _apply_repetition(self, doc: spacy.tokens.Doc) -> str:
        """Apply word repetition disfluency."""
        text = doc.text
        if len(text.strip()) == 0:
            return text

        order = random.choices(
            list(self.rep_order_probs.keys()),
            weights=list(self.rep_order_probs.values()),
        )[0]

        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.rep_pos_probs and i >= order - 1
        ]

        if not candidates:  # repeat random word
            idx = random.choice(range(len(text.split())))
            return text_ops.repeat_words(text, idx, 1)

        # Weight by POS probability
        try:
            weights = [self.rep_pos_probs[token.pos_] for _, token in candidates]
            idx, token = random.choices(candidates, weights=weights)[0]
            sentence = text_ops.repeat_words(text, idx - order + 1, order)
        except:
            print("Repetition failed for", text, order, idx)
            sentence = text

        return sentence

    def _apply_precorrection(self, doc: spacy.tokens.Doc) -> str:
        """Apply precorrection disfluency."""
        text = doc.text
        if len(text.strip()) == 0:
            return text

        candidates = [
            (i, token)
            for i, token in enumerate(doc)
            if token.pos_ in self.pre_pos_probs and len(token.text) > 4
        ]

        if not candidates:
            return text

        # Pre type
        pre_type = random.choices(
            list(self.pre_type_probs.keys()), weights=list(self.pre_type_probs.values())
        )[0]

        # Weight by POS probability
        weights = [self.pre_pos_probs[token.pos_] for _, token in candidates]
        idx, token = random.choices(candidates, weights=weights)[0]

        words = text.split()
        if pre_type == "CUT":
            words.insert(
                idx, text_ops.cut_word(token, cut_from_start=False, chars=True)
            )
        elif pre_type == "POS_CUT":
            words.insert(idx, text_ops.cut_word(token, cut_from_start=True, chars=True))
        elif pre_type == "PRE":
            sub_type = random.choices(
                list(self.sub_type_probs[token.pos_].keys()),
                weights=list(self.sub_type_probs[token.pos_].values()),
            )[0]

            try:
                words[idx] = text_ops.do_substitution(
                    token,
                    sub_type=sub_type,
                    nlp=self.nlp,
                    adj_inflection_probs=self.adj_inflection_probs,
                    verb_conjugation_probs=self.verb_conjugation_probs,
                    substitution_similarity_params=self.substitution_similarity_params,
                    char_patterns=self.char_patterns,
                    articles_map=self.articles_map,
                    prepositions=self.prepositions,
                    conjunctions=self.conjunctions,
                )
            except:
                print("Precorrection substitution failed for", token)
                pass

        return " ".join(words)

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

        return " ".join(words)
