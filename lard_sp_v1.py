import spacy
import random
import re
import random
import spacy_spanish_lemmatizer
from IPython import embed

class SpanishDisfluencyGenerator:
        def __init__(self):
            try:
                self.nlp = spacy.load('es_core_news_lg')
            except:
                print("Please install Spanish language model: python -m spacy download es_core_news_lg")
        
            # Common Spanish fillers
            self.fillers = ['e', 'a', 'em', 'ah']
            self.articles = ["el", "la", "las", "un", "una"]
            self.prepositions = ["de", "a", "en"]
            self.conjunctions = ["y", "que"]
            self.disc_markers = ["ay", "perdón", "ya", "digo"]
            self.phoneme_sust = {'c':'g', 
                                 'd':'t'}
            self.vowels = set('aeiouáéíóúüAEIOUÁÉÍÓÚÜ')
        
        def generate_DEL(self, sentence: str, pos_tag : dict) -> str:
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)
    
            del_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                      if token.pos_ in pos_tag and len(token.text) > 3]
    
            if not del_candidates:
                del_candidates = [(i, pos_tag.get(token.pos_, 0.05)) for i, token in enumerate(metadata) 
                          if token.pos_ in pos_tag]
    
            if not del_candidates and len(words) > 1:
                del_candidates = [(i, 1) for i in range(len(words)-1)]
    
            if del_candidates:
                idxs, probs = zip(*del_candidates)
                word_idx = random.choices(idxs, weights=probs)[0]
                result.pop(word_idx)
                return " ".join(result)
    
            return sentence
        
        def generate_SUST(self, sentence:str, pos_tag : dict)->str:

            if not sentence.strip():
                return sentence
            
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)

            sust_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                     if token.pos_ in pos_tag]
            
            if sust_candidates:
                idxs, probs = zip(*sust_candidates)
                word_idx = random.choices(idxs, weights=probs)[0]
                token = metadata[word_idx]

                if token.pos_ == 'VERB':
                    try:
                        if token.morph.get('VerbForm') == ['Fin']:
                            number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                            inflected = token._.inflect({'Number':number})
                            if inflected:
                                result[word_idx] = inflected
                        else:
                            inflected = token.lemma_ if token.text != token.lemma_ else token._.inflect('VerbForm=Fin')
                            if inflected:
                                result[word_idx] = inflected
                    except:
                        word = token.text
                        if 'a' in word: result[word_idx] = word.replace('a', 'e')
                        elif 'e' in word: result[word_idx] = word.replace('e', 'a')
                
                elif token.pos_ in ['NOUN', 'ADJ']:
                    try:
                        change_type = random.choices(['number', 'gender', 'spelling'], 
                                                     weights=[0.5, 0.3, 0.2])[0]
                        if change_type == 'number':
                            number = 'Sing' if 'Plur' in token.morph.get('Number',[]) else 'Plur'
                            inflected = token._.inflect({'Number':number})
                            if inflected:
                                result[word_idx] = inflected
                        elif change_type == 'gender': 
                            gender = 'Fem' if 'Masc' in token.morph.get('Gender', []) else 'Masc'
                            inflected = token._.inflect({'Gender': gender})
                            if inflected: 
                                result[word_idx] = inflected
                            else: 
                                word = token.text
                                if 'n' in word: 
                                    result[word_idx] = word.replace('n', 'm')
                    except:
                        word = token.text
                        if word.endswith('o'): result[word_idx] = word[:-1] + 'a'
                        elif word.endswith('a'): result[word_idx] = word[:-1] + 'o' 

                elif token.pos_ == 'DET':
                    det_map = {'la': 'una', 'una': 'la',
                                'el': 'un', 'un': 'el',
                                'los': 'las', 'las': 'los'}
                    if token.text.lower() in det_map:
                        result[word_idx] = det_map[token.text.lower()]

                elif token.pos_ == 'ADP':
                    prepositions = ['de', 'en', 'a', 'por', 'para', 'con', 'sin']
                    current_prep = prepositions.index(token.text) if token.text in prepositions else -1 
                    if current_prep >= 0:
                        available_preps = prepositions[:current_prep] + prepositions[current_prep+1:]
                        result[word_idx] = random.choice(available_preps)
            
            
            return " ".join(result)
               
        def generate_INS(self, sentence : str, insertion_probs : dict, target_pos : dict) -> str:
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)


            ins_candidates = [(i, token.pos_, token) for i, token in enumerate(metadata)
                              if token.pos_ in target_pos]
            
            if ins_candidates:
                idxs, pos_tags, tokens = zip(*ins_candidates)
                pos_weights = [target_pos[pos] for pos in pos_tags]
                target_idx = random.choices(range(len(idxs)), weights=pos_weights)[0]
                target_token = tokens[target_idx]

                word_type = random.choices(list(insertion_probs.keys()), 
                                           weights=list(insertion_probs.values()))[0]

                if word_type == 'articles' and target_token.pos_ in ['NOUN', 'ADJ']:
                    gender = target_token.morph.get('Gender',[''])[0]
                    number = target_token.morph.get('Number', [''])[0]

                    if gender == 'fem' and number == 'sing':
                        insert_word = random.choice(['la', 'una'])
                    elif gender == 'fem' and number == 'plur':
                        insert_word = random.choice(['las','unas'])
                    elif gender == 'masc' and number == 'sing':
                        insert_word = random.choice(['el','un'])
                    elif gender== 'masc' and number == 'plur':
                        insert_word = random.choice(['los', 'unos'])
                    else: 
                        insert_word = random.choice(self.articles)
                else:
                    if word_type == 'prepositions':
                        insert_word = random.choice(self.prepositions)
                    elif word_type == 'conjunctions':
                        insert_word = random.choice(self.conjunctions)
                    else: 
                        insert_word = random.choice(self.disc_markers)
                result.insert(idxs[target_idx], insert_word)
            
            return " ".join(result)

        def generate_CUT(self, sentence: str, dist: 0, pos_tag : dict) -> str:
            words = sentence.split()
            result = []
            metadata = self.nlp(sentence)
   
            cut_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                              if token.pos_ in pos_tag and len(token.text) > 3]
   
            if cut_candidates:
                idxs, probs = zip(*cut_candidates)
                word_idx = random.choices(idxs, weights=probs)[0]
                token = metadata[word_idx]
                cut_length = min(3, len(token.text) // 2)
                cut = token.text[:cut_length]
                cut_idx = max(0, word_idx - dist)
                for i, word in enumerate(words):
                     if i == cut_idx:
                         result.append(cut)
                     result.append(word)
            else:
                 result = words
               
            return " ".join(result)

        def generate_REP(self, sentence: str, pos_tag : dict) -> str:
            if not sentence or not sentence.strip():
                return sentence
            
            words = sentence.split()
            if not words:
                return sentence
            #words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)
    
            rep_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                     if token.pos_ in pos_tag]
    
            if rep_candidates:
                idxs, probs = zip(*rep_candidates)
                word_idx = random.choices(idxs, weights=probs)[0]
                word_to_repeat = words[word_idx]
                # inserta inmediatamente antes. Ver cómo hacer para hacer REP con distancia. 
                result.insert(word_idx, word_to_repeat)
    
            return " ".join(result)

        def generate_PRE(self, sentence: str, pos_tag : dict) -> str:
            
            if not sentence or not sentence.strip():
                return sentence
            
            words = sentence.split()
            if not words:
                return sentence
            
            #words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence) 
            
            if not sentence.strip():
                return sentence

            pre_candidates = []
            for i, token in enumerate(metadata):
                if token.pos_ not in pos_tag:
                    continue
                if token.pos_ and i < len(words):
                    pre_candidates.append((i, pos_tag[token.pos_]))
            
            if pre_candidates:
                idxs, probs = zip(*pre_candidates)
                word_idx = random.choices(idxs, weights=probs)[0]
                token = metadata[word_idx]
                target_word = words[word_idx]

                first_syllable = target_word[:2] if len(target_word) > 2 else target_word
                vowels = [c for c in target_word if c in 'aeiouáéíóú']

                pre_types = [
                    lambda w: w.replace('e', 'a').replace('o', 'u'),
                    lambda w: w.replace('e', 'o').replace('i', 'u'),
                    lambda w: first_syllable.replace('e', 'a') + w[2:4],
                    lambda w: first_syllable.replace('o', 'u') + w[2:4],
                    lambda w: w[:2] + random.choice(['s', 't', 'd']) + w[2:],
                    lambda w: w[:4].replace('e', 'a'),
                    lambda w: w[:3].replace('n', 'r'),
                    lambda w: w.replace('nt', 'nd').replace('mp', 'mb')]

                try:
                    transform_func = random.choice(pre_types)
                    pre_word = transform_func(target_word)
                    if pre_word != target_word:  # Only insert if word was actually changed
                        result.insert(word_idx, pre_word)
                except Exception as e:
                    print(f"Error transforming word '{target_word}': {str(e)}")
                    return sentence
            
            return " ".join(result)

        def generate_FILL(self, sentence : str) -> str:
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)
            # TODO: Implement filler generation associated to POS and frequency
            # fillers appear before Adpositions (30.77%) and Nouns (23.08%) and 
            # equally distributed (7.69%) among PRON, ADJ, CCONJ and VERB. 
            # Most common filler is 'e' followed by 'a'. 
            index = random.randint(0, len(words))
            result.insert(index, random.choice(self.fillers))
            return ' '.join(result)


   

def main():
    dg = SpanishDisfluencyGenerator()
    input_text = '../../textos/5_grado.txt'
    output_text = '../../textos/5_grado_disfluent.txt'
    
    with open(input_text, 'r', encoding='utf-8') as f:
        text = f.read()
    
    sentences = [s.strip() for s in text.split('.') if s.strip()]

    #pos_tag_del = {'DET': 0.35, 'NOUN':0.10, 'ADP': 0.15, 'CCONJ': 0.15, 'PRON': 0.10, 'AUX': 0.05}
    #pos_tag_sust = {'VERB':0.25, 'NOUN':0.20, 'ADJ':0.15, 'DET':0.12, 'ADP':0.08}
    #Target pos es el pos tag que aparece más frecuentemente después de una inserción
    #target_pos_ins = {'NOUN':0.35, 'DET':0.25, 'ADJ':0.20, 'VERB':0.15, 'ADP':0.05}
    #Son los pos tags más frecuentemente insertados
    #insertion_probs = {'articles':0.40, 'prepositions': 0.30, 'conjunctions':0.20, 'disc_markers':0.10} 
    #pos_tag_cut = {'VERB': 0.35, 'NOUN': 0.30, 'ADJ': 0.25, 'ADP': 0.05, 'DET': 0.05}
    #pos_tag_rep = {'ADP': 0.35, 'DET': 0.30, 'VERB': 0.15, 'AUX': 0.10, 'NOUN': 0.10}
    # pos_tag_pre = {'VERB': 0.30, 'NOUN': 0.25, 'ADJ': 0.15, 'ADP': 0.10, 'DET': 0.10, 'AUX': 0.05, 'PRON': 0.05, 'NUM': 0.05, 'ADV': 0.05}   

    # ALL
    #pos_tag_del = {'DET': 0.28, 'NOUN':0.10, 'ADP': 0.22, 'CCONJ': 0.09, 'PRON': 0.10, 'AUX': 0.05}
    #pos_tag_sust = {'VERB':0.21, 'NOUN':0.28, 'ADJ':0.14, 'DET':0.12, 'ADP':0.06}
    #Target pos es el pos tag que aparece más frecuentemente después de una inserción
    #target_pos_ins = {'NOUN':0.29, 'DET':0.19, 'ADJ':0.08, 'VERB':0.10, 'ADP':0.06}
    #Son los pos tags más frecuentemente insertados
    #insertion_probs = {'articles':0.37, 'prepositions': 0.17, 'conjunctions':0.10, 'disc_markers':0.10} 
    #pos_tag_cut = {'VERB': 0.25, 'NOUN': 0.25, 'ADJ': 0.31, 'ADP': 0.05, 'DET': 0.06}
    #pos_tag_rep = {'ADP': 0.31, 'DET': 0.14, 'VERB': 0.10, 'AUX': 0.08, 'NOUN': 0.10}
    #pos_tag_pre = {'VERB': 0.14, 'NOUN': 0.31, 'ADJ': 0.11, 'ADP': 0.06, 'DET': 0.01, 'AUX': 0.05, 'PRON': 0.05, 'NUM': 0.05, 'ADV': 0.02}   

    # PRIMERO
    #pos_tag_del = {'DET': 0.27, 'NOUN':0.08, 'ADP': 0.29, 'CCONJ': 0.05, 'PRON': 0.10, 'AUX': 0.05}
    #pos_tag_sust = {'VERB':0.24, 'NOUN':0.24, 'ADJ':0.19, 'DET':0.11, 'ADP':0.08}
    #Target pos es el pos tag que aparece más frecuentemente después de una inserción
    #target_pos_ins = {'NOUN':0.28, 'DET':0.22, 'ADJ':0.02, 'VERB':0.12, 'ADP':0.07}
    #Son los pos tags más frecuentemente insertados
    #insertion_probs = {'articles':0.31, 'prepositions': 0.23, 'conjunctions':0.11, 'disc_markers':0.10} 
    #pos_tag_cut = {'VERB': 0.41, 'NOUN': 0.21, 'ADJ': 0.25, 'ADP': 0.10, 'DET': 0.03}
    #pos_tag_rep = {'ADP': 0.41, 'DET': 0.08, 'VERB': 0.17, 'AUX': 0.09, 'NOUN': 0.08}
    #pos_tag_pre = {'VERB': 0.25, 'NOUN': 0.37, 'ADJ': 0.12, 'ADP': 0.12, 'DET': 0.01, 'AUX': 0.01, 'PRON': 0.05, 'NUM': 0.05, 'ADV': 0.05}   

    # TERCERO
    #pos_tag_del = {'DET': 0.18, 'NOUN':0.13, 'ADP': 0.17, 'CCONJ': 0.16, 'PRON': 0.06, 'AUX': 0.02}
    #pos_tag_sust = {'VERB':0.22, 'NOUN':0.41, 'ADJ':0.12, 'DET':0.11, 'ADP':0.05}
    #Target pos es el pos tag que aparece más frecuentemente después de una inserción
    #target_pos_ins = {'NOUN':0.35, 'DET':0.21, 'ADJ':0.08, 'VERB':0.09, 'ADP':0.04}
    #Son los pos tags más frecuentemente insertados
    #insertion_probs = {'articles':0.34, 'prepositions': 0.18, 'conjunctions':0.17, 'disc_markers':0.10} 
    #pos_tag_cut = {'VERB': 0.19, 'NOUN': 0.26, 'ADJ': 0.35, 'ADP': 0.01, 'DET': 0.11}
    #pos_tag_rep = {'ADP': 0.14, 'DET': 0.22, 'VERB': 0.11, 'AUX': 0.10, 'NOUN': 0.13}
    #pos_tag_pre = {'VERB': 0.12, 'NOUN': 0.29, 'ADJ': 0.12, 'ADP': 0.06, 'DET': 0.01, 'AUX': 0.03, 'PRON': 0.01, 'NUM': 0.05, 'ADV': 0.05}   

    # QUINTO
    pos_tag_del = {'DET': 0.42, 'NOUN':0.12, 'ADP': 0.13, 'CCONJ': 0.08, 'PRON': 0.24, 'AUX': 0.02}
    pos_tag_sust = {'VERB':0.17, 'NOUN':0.17, 'ADJ':0.12, 'DET':0.18, 'ADP':0.06}
    #Target pos es el pos tag que aparece más frecuentemente después de una inserción
    target_pos_ins = {'NOUN':0.25, 'DET':0.11, 'ADJ':0.17, 'VERB':0.08, 'ADP':0.07}
    #Son los pos tags más frecuentemente insertados
    insertion_probs = {'articles':0.47, 'prepositions': 0.09, 'conjunctions':0.03, 'disc_markers':0.10} 
    pos_tag_cut = {'VERB': 0.18, 'NOUN': 0.26, 'ADJ': 0.31, 'ADP': 0.03, 'DET': 0.04}
    pos_tag_rep = {'ADP': 0.40, 'DET': 0.11, 'VERB': 0.03, 'AUX': 0.03, 'NOUN': 0.09, 'PRON': 0.22}
    pos_tag_pre = {'VERB': 0.12, 'NOUN': 0.28, 'ADJ': 0.09, 'ADP': 0.02, 'DET': 0.02, 'AUX': 0.07, 'PRON': 0.05, 'NUM': 0.05, 'ADV': 0.05}   



    
    methods_all = [
        ('DEL', lambda s: dg.generate_DEL(s, pos_tag_del)),
        ('SUST', lambda s: dg.generate_SUST(s, pos_tag_sust)),
        ('INS', lambda s: dg.generate_INS(s, insertion_probs, target_pos_ins)),
        ('CUT', lambda s: dg.generate_CUT(s, 0, pos_tag_cut)),
        ('REP', lambda s: dg.generate_REP(s, pos_tag_rep)),
        ('PRE', lambda s: dg.generate_PRE(s, pos_tag_pre)),
        ('FILL', lambda s: dg.generate_FILL(s))
    ]

    
    with open(output_text, 'w') as out_f:
        for sentence in sentences:

            for _, method_func in methods_all:
                for _ in range(10):  
                    try:
                        modified = method_func(sentence)
                        if modified != sentence:  
                            out_f.write(f"{modified}\n")
                    except Exception as e:
                        continue
            
            out_f.write("")

if __name__ == "__main__":
    main()