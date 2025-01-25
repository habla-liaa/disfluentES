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
            self.prepositions = ['a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'hacia', 'hasta', 'para', 'por', 'según', 'sin', 'sobre', 'tras']   
            self.conjunctions = { 'CCONJ': ['y', 'e', 'ni', 'o', 'u', 'pero', 'sino', 'mas', 'aunque', 'si bien', 'por más que'],
                                 'SCONJ': ['que', 'porque', 'pues', 'ya que', 'puesto que', 'si', 'como', 'cuando', 'siempre que', 'mientras', 'antes que', 
                                           'después que', 'aunque', 'si bien', 'por más que', 'para que', 'a fin de que', 'como', 'tal como', 'así como']}

            self.disc_markers = ['ay', 'perdón', 'ya', 'digo', 'no']
            self.char_sust = {'c':'g', 
                                 'd':'t'}
            self.vowels = set('aeiouáéíóúüAEIOUÁÉÍÓÚÜ')
            self.char_patterns = {'substitutions': {'consonants': {'n': {'d', 'g', 'l', 'r', 't'},
                                                                    't': {'d', 'p'},
                                                                    'j': {'g', 's'},
                                                                   'c': {'s', 'z', 'q'},
                                                                   'm': {'n', 'p', 'x'},
                                                                   'mp': {'mb', 'p', 'b'},
                                                                   'b': {'d', 'p', 'f'},
                                                                   'r': {'l', 'n', 'd'},
                                                                   'l': {'r', 'n', 'd'},
                                                                   'd': {'t', 'b'},
                                                                   'p': {'b', 't', 'f'},
                                                                   's': {'x', 'd'},
                                                                   'v': {'f'}, 
                                                                   'r': {'l', 'n', 'd', 'rr'}, 
                                                                   'ce': {'que'}},

                                                    'vowels': {'i': {'e', 'y'},
                                                               'u': {'e', 'o','i'},
                                                               'a': {'i', 'e', 'o'},
                                                               'e': {'a', 'o', 'i', 'ie'},
                                                               'o': {'u', 'a', 'io'}},
                                                    'diphthongs': {'ie': {'e', 'ei'},
                                                                   'ue': {'u', 'o', 'e'},
                                                                   'ai': {'ae'},
                                                                   'ei': {'ie', 'e', 'i'},
                                                                   'io': {'i', 'o'}}
                                                               
                                                               },

                                                    'insertions': {
                                                        'position': {'start': {'p', 'e', 'a', 'c', 'd', 'v'},
                                                                 'middle': {'i', 'r', 'u', 'e', 'n', 's'},
                                                                 'end': {'n', 's', 'o'}}},
                                                    'deletions': {'position': {
                                                                        'start': {'a', 'e', 'p'},
                                                                        'middle': {'n','r', 'p', 'c', 'i', 'e', 'n', 'x', 's'},
                                                                        'end': {'s', 'z', 'o', 'a', 'e', 'r'} }}}

        
        def _inflect_word(word):
            if 'verb': 
                pass
            if ['noun', 'adj']:
                pass
            return word
    
 
        def _sust_char():
            pass

        def _cut_word(): 
            pass


        def _delete_char():
            pass

        def _insert_char():
            pass

        def _delete_char():
            pass
        def generate_DEL(self, sentence: str, pos_tag : dict) -> str:
            # A Veces no encuentra candidatos para eliminar.
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)

            del_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                      if token.pos_ in pos_tag and len(token.text) > 3]
    
            idxs, probs = zip(*del_candidates)
            word_idx = random.choices(idxs, weights=probs)[0]
            result.pop(word_idx)
            return " ".join(result)
    
            return sentence

        
        def generate_PHO(self, sentence:str, pos_tag : dict)->str:
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)

            pho_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                     if token.pos_ in pos_tag]
            idxs, probs = zip(*pho_candidates)
            word_idx = random.choices(idxs, weights=probs)[0]
            token = metadata[word_idx]

            # 

            # tirar una moneda pesada y elegir si inserción, sustitución, deletion, permutación
            # Suelen ser: 
            # sustituciones de consonantes vocales o diptongos
            # inserciones al comienzo o al final y en el medio
            # deletions al comienzo, en el medio o al final
        
            # 


        def generate_SUST(self, sentence:str, pos_tag : dict)->str:
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)

            sust_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                     if token.pos_ in pos_tag]
            
            idxs, probs = zip(*sust_candidates)
            word_idx = random.choices(idxs, weights=probs)[0]
            token = metadata[word_idx]

            # tirar una moneda pesada y elegir si misspelling, inflect o familia de palabras.
            alteration_subclass = {'misspelling': 0.3, 'inflection': 0.5, 'similarity': 0.2}
            alteration = random.choices(list(alteration_subclass.keys()), weights=list(alteration_subclass.values()))[0]
            

            if token.pos_ in ['VERB', 'AUX']:
                # (30) sustitución por verbos similares en la misma conjugación. 
                # (25) sustitución de verbo es el agreement de número. Cambiar de plural a singluar y al reves. 
                # (20) Después lo que ocurre es que puede cambiar de tiempo verbal: pasado a presente, presente a pasado
                # (15) Hay algunas nominalizaciones. Si el verbo es infinitivo se puede cambiar a un sustantivo de misma raíz. 
                # (10) Mal pronunciar o volver reflexivo 
                pass

            if token.pos_ in ['NOUN', 'ADJ']:
                # (40) genero y numero
                # (60) palabras similares y MUY similares (30). Las MUY similares son edit distance 1 (30). Las similares pueden ser
                # solo similares de caracteres o de un campo semantico similar. 
                # Generar un misspelling severo

            if token.pos_ == ['DET', 'PRON']:
                # Solo cambiar genero (35)
                # Cambiar número (30)
                # Cambiar por otro determinante manteniendo genero y numero la/una, el/un, los/unos, las/unas (20)
                
            if token_pos_ == ['ADP']:
                # Cambiar por otra preposición o conjunción 
                pass
        
            if token_pos_ in ['CCONJ', 'SCONJ']:
                # Cambiar por otro a
                pass

            else: 
                # Agarrar la palabra y buscar otra similar. 
           
            
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
                # CUT

               
            return " ".join(result)

        def generate_REP(self, sentence: str, pos_tag : dict) -> str:      
            words = sentence.split()
            result = words.copy()
            metadata = self.nlp(sentence)
    
            rep_candidates = [(i, pos_tag[token.pos_]) for i, token in enumerate(metadata) 
                     if token.pos_ in pos_tag]
    
            idxs, probs = zip(*rep_candidates)
            word_idx = random.choices(idxs, weights=probs)[0]
            word_to_repeat = words[word_idx]
            # inserta inmediatamente antes. Ver cómo hacer para hacer REP con distancia. 
            result.insert(word_idx, word_to_repeat)
    
            return " ".join(result)

        # EL PRE puede ser un CUT permutado o con alguna transformación fonética loca. 
        def generate_PRE(self, sentence: str, pos_tag : dict) -> str:
            
            if not sentence or not sentence.strip():
                return sentence
            
            words = sentence.split()
            if not words:
                return sentence
            
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

                
            pre_type = ['PRE', 'CUT']
            pre = random.choices(pre_type, weights=[0.2, 0.8])[0]
            if pre == 'PRE':
                # genera un CUT + PHO
                # PHO
                # S
          
            else:
                # CUT
                

            
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