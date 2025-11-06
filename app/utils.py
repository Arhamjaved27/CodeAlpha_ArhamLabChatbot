import spacy
import re
from typing import List


def load_spacy_model():
    """Load SpaCy English model"""
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        raise OSError(
            "SpaCy English model not found. Please install it using: "
            "python -m spacy download en_core_web_sm"
        )
    return nlp


def preprocess_text(text: str, nlp) -> str:
    """
    Preprocess text using SpaCy:
    - Tokenize
    - Lemmatize
    - Remove stopwords
    - Remove punctuation and special characters
    - Convert to lowercase
    """
    # Process text with SpaCy
    doc = nlp(text.lower())
    
    # Extract lemmatized tokens, excluding stopwords and punctuation
    tokens = [
        token.lemma_ 
        for token in doc 
        if not token.is_stop 
        and not token.is_punct 
        and not token.is_space
        and len(token.lemma_) > 1
    ]
    
    # Join tokens back into a string
    return " ".join(tokens)


def clean_text(text: str) -> str:
    """Basic text cleaning - remove extra whitespace"""
    return re.sub(r'\s+', ' ', text.strip())

