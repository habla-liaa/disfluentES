import json
import pickle
import pandas as pd
from IPython import embed
import spacy

verbos = [
    ("Indicativo", "Indicativo presente", "yo", "camino"),
    ("Indicativo", "Indicativo presente", "tú", "caminas"),
    ("Indicativo", "Indicativo presente", "él", "camina"),
    ("Indicativo", "Indicativo presente", "nosotros", "caminamos"),
    ("Indicativo", "Indicativo presente", "vosotros", "camináis"),
    ("Indicativo", "Indicativo presente", "ellos", "caminan"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "yo", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "tú", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "él", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "nosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "vosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto compuesto", "ellos", "caminado"),
    ("Indicativo", "Indicativo pretérito imperfecto", "yo", "caminaba"),
    ("Indicativo", "Indicativo pretérito imperfecto", "tú", "caminabas"),
    ("Indicativo", "Indicativo pretérito imperfecto", "él", "caminaba"),
    ("Indicativo", "Indicativo pretérito imperfecto", "nosotros", "caminábamos"),
    ("Indicativo", "Indicativo pretérito imperfecto", "vosotros", "caminabais"),
    ("Indicativo", "Indicativo pretérito imperfecto", "ellos", "caminaban"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "yo", "caminado"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "tú", "caminado"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "él", "caminado"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "nosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "vosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito pluscuamperfecto", "ellos", "caminado"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "yo", "caminé"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "tú", "caminaste"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "él", "caminó"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "nosotros", "caminamos"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "vosotros", "caminasteis"),
    ("Indicativo", "Indicativo pretérito perfecto simple", "ellos", "caminaron"),
    ("Indicativo", "Indicativo pretérito anterior", "yo", "caminado"),
    ("Indicativo", "Indicativo pretérito anterior", "tú", "caminado"),
    ("Indicativo", "Indicativo pretérito anterior", "él", "caminado"),
    ("Indicativo", "Indicativo pretérito anterior", "nosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito anterior", "vosotros", "caminado"),
    ("Indicativo", "Indicativo pretérito anterior", "ellos", "caminado"),
    ("Indicativo", "Indicativo futuro", "yo", "caminaré"),
    ("Indicativo", "Indicativo futuro", "tú", "caminarás"),
    ("Indicativo", "Indicativo futuro", "él", "caminará"),
    ("Indicativo", "Indicativo futuro", "nosotros", "caminaremos"),
    ("Indicativo", "Indicativo futuro", "vosotros", "caminaréis"),
    ("Indicativo", "Indicativo futuro", "ellos", "caminarán"),
    ("Indicativo", "Indicativo futuro perfecto", "yo", "caminado"),
    ("Indicativo", "Indicativo futuro perfecto", "tú", "caminado"),
    ("Indicativo", "Indicativo futuro perfecto", "él", "caminado"),
    ("Indicativo", "Indicativo futuro perfecto", "nosotros", "caminado"),
    ("Indicativo", "Indicativo futuro perfecto", "vosotros", "caminado"),
    ("Indicativo", "Indicativo futuro perfecto", "ellos", "caminado"),
    ("Subjuntivo", "Subjuntivo presente", "yo", "camine"),
    ("Subjuntivo", "Subjuntivo presente", "tú", "camines"),
    ("Subjuntivo", "Subjuntivo presente", "él", "camine"),
    ("Subjuntivo", "Subjuntivo presente", "nosotros", "caminemos"),
    ("Subjuntivo", "Subjuntivo presente", "vosotros", "caminéis"),
    ("Subjuntivo", "Subjuntivo presente", "ellos", "caminen"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "yo", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "tú", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "él", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "nosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "vosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito perfecto", "ellos", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "yo", "caminara"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "tú", "caminaras"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "él", "caminara"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "nosotros", "camináramos"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "vosotros", "caminarais"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 1", "ellos", "caminaran"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "yo", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "tú", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "él", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "nosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "vosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 1", "ellos", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "yo", "caminase"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "tú", "caminases"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "él", "caminase"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "nosotros", "caminásemos"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "vosotros", "caminaseis"),
    ("Subjuntivo", "Subjuntivo pretérito imperfecto 2", "ellos", "caminasen"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "yo", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "tú", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "él", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "nosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "vosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo pretérito pluscuamperfecto 2", "ellos", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro", "yo", "caminare"),
    ("Subjuntivo", "Subjuntivo futuro", "tú", "caminares"),
    ("Subjuntivo", "Subjuntivo futuro", "él", "caminare"),
    ("Subjuntivo", "Subjuntivo futuro", "nosotros", "camináremos"),
    ("Subjuntivo", "Subjuntivo futuro", "vosotros", "caminareis"),
    ("Subjuntivo", "Subjuntivo futuro", "ellos", "caminaren"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "yo", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "tú", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "él", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "nosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "vosotros", "caminado"),
    ("Subjuntivo", "Subjuntivo futuro perfecto", "ellos", "caminado"),
    ("Imperativo", "Imperativo Afirmativo", "tú", "camina"),
    ("Imperativo", "Imperativo Afirmativo", "él", "camine"),
    ("Imperativo", "Imperativo Afirmativo", "nosotros", "caminemos"),
    ("Imperativo", "Imperativo Afirmativo", "vosotros", "caminad"),
    ("Imperativo", "Imperativo Afirmativo", "ellos", "caminen"),
    ("Imperativo", "Imperativo non", "tú no", "camines"),
    ("Imperativo", "Imperativo non", "él no", "camine"),
    ("Imperativo", "Imperativo non", "nosotros no", "caminemos"),
    ("Imperativo", "Imperativo non", "vosotros no", "caminéis"),
    ("Imperativo", "Imperativo non", "ellos no", "caminen"),
    ("Condicional", "Condicional Condicional", "yo", "caminaría"),
    ("Condicional", "Condicional Condicional", "tú", "caminarías"),
    ("Condicional", "Condicional Condicional", "él", "caminaría"),
    ("Condicional", "Condicional Condicional", "nosotros", "caminaríamos"),
    ("Condicional", "Condicional Condicional", "vosotros", "caminaríais"),
    ("Condicional", "Condicional Condicional", "ellos", "caminarían"),
    ("Condicional", "Condicional perfecto", "yo", "caminado"),
    ("Condicional", "Condicional perfecto", "tú", "caminado"),
    ("Condicional", "Condicional perfecto", "él", "caminado"),
    ("Condicional", "Condicional perfecto", "nosotros", "caminado"),
    ("Condicional", "Condicional perfecto", "vosotros", "caminado"),
    ("Condicional", "Condicional perfecto", "ellos", "caminado"),
    ("Infinitivo", "Infinitivo Infinitivo", "", "caminar"),
    ("Gerundio", "Gerundio Gerondio", "", "caminando"),
    ("Participo", "Participo Participo", "", "caminado"),
]


nlp = spacy.load("es_core_news_lg")

data = []
for verb in verbos:
    d = {
        "verb": verb[3],
        "tense": verb[1].replace(verb[0], ""),
        "mood": verb[0],
        "person": verb[2],
    }
    d.update(nlp(verb[3])[0].morph.to_dict())
    data.append(d)

df = pd.DataFrame(data)

df.to_csv("scripts/verbs_table.csv", index=False)

df = pd.read_csv("scripts/verbs_table_real.csv")


dfx = df[["VerbForm", "Mood","Tense","Person", "Number", "tense", "mood", "person"]].value_counts().reset_index().drop("count",axis=1).set_index(["VerbForm", "Mood","Tense","Person", "Number"]).sort_index()

# spacy_to_mlconjug3 = {k: g.to_dict(orient='records') for k, g in dfx.groupby(level=(0,1))}
spacy_to_mlconjug3 = dfx.T.to_dict()

print(spacy_to_mlconjug3)

# save pickle
with open("scripts/spacy_to_mlconjug3.pkl", "wb") as f:
    pickle.dump(spacy_to_mlconjug3, f)
