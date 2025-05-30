"""Main Spanish disfluency generator module."""

import copy
import random
from IPython import embed
import numpy as np
import spacy
import gin
from typing import Optional, Dict, List, Union, Set
from .operations import phonological, spacy_es_wrong_pos, default_char_patterns
from .operations import text as text_ops
# from spacy_syllables import SpacySyllables


@gin.configurable
class SpanishDisfluencyGenerator:
    """Generator class for Spanish disfluencies."""

    def __init__(
        self,
        seed: int = 42,
        recursive_depth: int = 1,
        disfluency_type_probs: Dict[str, float] = None,
        disfluency_uniform: List[str] = None,
        disfluency_sequence: List[str] = None,
        del_pos_probs: Dict[str, float] = None,
        pho_pos_probs: Dict[str, float] = None,
        sub_pos_probs: Dict[str, Dict[str, float]] = None,
        sub_type_probs: Dict[str, Dict[str, float]] = None,
        adj_inflection_probs: Dict[str, float] = None,
        verb_conjugation_probs: Dict[str, float] = None,
        articles_map: Dict[str, List[str]] = None,
        ins_type_probs: Dict[str, float] = None,
        ins_pos_probs: Dict[str, float] = None,
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
            recursive_depth: Number of repeated disfluencies to apply
            disfluency_type_probs: Probabilities for disfluency types
            disfluency_uniform: List of specific disfluency types to apply num_variations times (defaults to None)
            disfluency_sequence: List of specific disfluency types to apply num_repetitions times in order.
            del_pos_probs: POS tag probabilities for deletion
            pho_pos_probs: POS tag probabilities for phonological changes
            sub_pos_probs: POS tag and type probabilities for substitution
            sub_type_probs: Substitution type probabilities
            adj_inflection_probs: Probabilities for noun inflection
            verb_conjugation_probs: Probabilities for verb conjugation
            ins_type_probs: Probabilities for insertion types
            ins_pos_probs: Target POS probabilities for insertion
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
            # self.nlp.add_pipe("syllables", after="ner")
        except OSError:
            raise OSError(
                "Please install Spanish language model: python -m spacy download es_core_news_lg"
            )

        random.seed(seed)
        np.random.seed(seed)
        
        self.recursive_depth = recursive_depth
        
        self.disfluency_uniform = disfluency_uniform
        self.disfluency_sequence = disfluency_sequence  
        self.disfluency_type_probs = disfluency_type_probs

        # Load POS probabilities from gin config
        self.del_pos_probs = del_pos_probs
        self.pho_pos_probs = pho_pos_probs
        self.sub_pos_probs = sub_pos_probs
        self.sub_type_probs = sub_type_probs
        self.adj_inflection_probs = adj_inflection_probs
        self.verb_conjugation_probs = verb_conjugation_probs
        self.ins_type_probs = ins_type_probs
        self.ins_pos_probs = ins_pos_probs
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
        self,
        text: str,
        num_variations: Optional[int] = None,
        leave_original_ratio: float = 0.0,
    ) -> str:
        """Generate disfluencies in the input text.

        Args:
            text: Input text to add disfluencies to
            num_variations: Number of variations to apply (defaults to 1)

        Returns:
            Text with added disfluencies
        """
        if not text:
            return text

        num_variations = num_variations or 1

        doc = self.parse_text(text)

        results = []

        if self.disfluency_uniform:
            for disfluency in self.disfluency_uniform:
                for _ in range(num_variations):
                    if random.random() < leave_original_ratio:
                        results.append(text)
                    else:
                        result_text = self._apply_disfluency(disfluency, doc)
                        results.append(result_text)

        elif self.disfluency_sequence:
            # Deterministic mode: apply specified disfluencies in order
            doc_original = copy.deepcopy(doc)
            for _ in range(num_variations):
                doc = doc_original
                for disfluency in self.disfluency_sequence:
                    result_text = self._apply_disfluency(disfluency, doc)
                    doc = self.nlp(result_text)
                results.append(result_text)
        elif self.disfluency_type_probs:
            # Random mode: choose disfluencies based on probabilities
            doc_original = copy.deepcopy(doc)
            for _ in range(num_variations):
                doc = doc_original
                if random.random() < leave_original_ratio:
                    results.append(text)
                else:
                    for _ in range(self.recursive_depth):
                        disfluency = random.choices(
                            list(self.disfluency_type_probs.keys()),
                            weights=list(self.disfluency_type_probs.values()),
                        )[0]

                        # done = False
                        # while not done:
                            # try:
                        result_text = self._apply_disfluency(disfluency, doc)
                        doc = self.nlp(result_text)
                                # done = True
                            #  except Exception as e:
                            #     print(
                            #         "Disfluency failed for",
                            #         disfluency,
                            #         doc.text,
                            #         "with exception",
                            #         e,
                            #     )
                            #     pass
                    results.append(result_text)

        else:
            raise ValueError("No disfluency setting provided")

        return results

    def _apply_disfluency(self, disfluency: str, doc: spacy.tokens.Doc) -> str:
        """Apply a specific disfluency type."""

        if disfluency == "DEL" and self.del_pos_probs is not None:
            return self._apply_deletion(doc)
        elif disfluency == "PHO" and self.pho_pos_probs is not None:
            return self._apply_phonological(doc)
        elif (
            disfluency == "SUB"
            and self.sub_pos_probs is not None
            and self.sub_type_probs is not None
        ):
            return self._apply_substitution(doc)
        elif (
            disfluency == "INS"
            and self.ins_type_probs is not None
            and self.ins_pos_probs is not None
        ):
            return self._apply_insertion(doc)
        elif disfluency == "CUT" and self.cut_pos_probs is not None:
            return self._apply_cut(doc)
        elif (
            disfluency == "REP"
            and self.rep_pos_probs is not None
            and self.rep_order_probs is not None
        ):
            return self._apply_repetition(doc)
        elif (
            disfluency == "PRE"
            and self.pre_pos_probs is not None
            and self.pre_type_probs is not None
        ):
            return self._apply_precorrection(doc)
        elif disfluency == "FILL" and self.fillers is not None:
            return self._apply_filler(doc)
        else:
            print("Disfluency type not set", disfluency)
            print("rep pos prob:",self.rep_pos_probs)
            print("pre pos prob:",self.pre_pos_probs)
            print("ins pos prob:",self.ins_pos_probs)
            print("cut pos prob:",self.cut_pos_probs)
            print("sub pos prob:",self.sub_pos_probs)
            print("pho pos prob:",self.pho_pos_probs)
            print("del pos prob:",self.del_pos_probs)
            print("rep order prob:",self.rep_order_probs)
            print("pre type prob:",self.pre_type_probs)
            print("sub type prob:",self.sub_type_probs)
            print("ins type prob:",self.ins_type_probs)
            raise ValueError("Disfluency type not set")

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
        except Exception as e:
            print(doc.text)
            print("Substitution failed for", token, "with sub_type", sub_type, "with exception")
            print(e)
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
            if token.pos_ in self.ins_pos_probs
        ]

        if not candidates:
            return text

        # Weight by POS probability
        weights = [self.ins_pos_probs[pos] for _, pos, _ in candidates]
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
            print("no candidates")
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
            if token.pos_ in self.sub_type_probs:
                sub_type = random.choices(
                    list(self.sub_type_probs[token.pos_].keys()),
                    weights=list(self.sub_type_probs[token.pos_].values()),
                )[0]
            else:
                sub_type = random.choice(list(self.sub_type_probs.keys()))

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

        try:
            " ".join(words)
        except:
            embed()

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
