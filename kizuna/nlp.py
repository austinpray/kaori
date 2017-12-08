
# https://spacy.io/api/annotation
taggable_pos = [
    'ADJ',
    'INTJ',
    'NOUN',
    'PROPN',
    'VERB',
    'X'
]


def extract_possible_tags(nlp, text):
    doc = nlp(text)
    return [token for token in doc if token.pos_ in taggable_pos]
