import json
import os
import re
from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.models import FAQ
from app.utils import load_spacy_model, preprocess_text


class FAQChatbot:
    """FAQ Chatbot using TF-IDF and cosine similarity"""
    
    def __init__(self, faqs_file: str = None):
        """
        Initialize the chatbot
        
        Args:
            faqs_file: Path to the JSON file containing FAQs (relative to project root)
        """
        if faqs_file is None:
            # Get the project root directory (parent of app directory)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            faqs_file = os.path.join(project_root, "data", "faqs.json")
        
        if not os.path.isabs(faqs_file):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            faqs_file = os.path.join(project_root, faqs_file)

        self.faqs_file = faqs_file
        self.faqs: List[FAQ] = []
        self.nlp = load_spacy_model()
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = None
        self.processed_questions = []
        self.greeting_response = "Hello! How can I help you today?"
        self.goodbye_response = "Goodbye! If you need anything else, just ask. Have a great day!"

        self._greeting_patterns = re.compile(r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b", re.I)
        self._goodbye_patterns = re.compile(r"\b(bye|goodbye|see you|see ya|take care|farewell)\b", re.I)

        self.load_faqs()
        self.build_index()
    
    def load_faqs(self):
        """Load FAQs from JSON file"""
        if not os.path.exists(self.faqs_file):
            raise FileNotFoundError(f"FAQ file not found: {self.faqs_file}")
        
        with open(self.faqs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.faqs = [FAQ(**faq) for faq in data.get("faqs", [])]
        
        if not self.faqs:
            raise ValueError("No FAQs found in the file")
    
    def build_index(self):
        """Build TF-IDF index from FAQ questions"""
        # Preprocess all FAQ questions
        self.processed_questions = [
            preprocess_text(faq.question, self.nlp) 
            for faq in self.faqs
        ]
        
        # Build TF-IDF vectors
        self.faq_vectors = self.vectorizer.fit_transform(self.processed_questions)
    
    def find_best_match(self, user_question: str, threshold: float = 0.1) -> Tuple[Optional[FAQ], float]:
        """
        Find the best matching FAQ for a user question
        
        Args:
            user_question: The user's question
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            Tuple of (best_matching_faq, confidence_score)
        """
        # Preprocess user question
        processed_question = preprocess_text(user_question, self.nlp)
        
        # Vectorize user question
        user_vector = self.vectorizer.transform([processed_question])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.faq_vectors)[0]
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_score = float(similarities[best_idx])
        
        # Return match if above threshold
        if best_score >= threshold:
            return self.faqs[best_idx], best_score
        
        return None, best_score
    
    def get_response(self, user_question: str) -> dict:
        """
        Get chatbot response for user question
        
        Args:
            user_question: The user's question
        
        Returns:
            Dictionary with answer, confidence, and metadata
        """
        if not user_question.strip():
            return {
                "answer": "Please ask a question.",
                "confidence": 0.0,
                "matched_question": None,
                "category": None
            }

        # Check for simple conversational intents (greeting / goodbye)
        # Use simple regex matching so we don't rely on the TF-IDF index for short chit-chat
        if self._greeting_patterns.search(user_question):
            return {
                "answer": self.greeting_response,
                "confidence": 1.0,
                "matched_question": None,
                "category": "smalltalk:greeting"
            }

        if self._goodbye_patterns.search(user_question):
            return {
                "answer": self.goodbye_response,
                "confidence": 1.0,
                "matched_question": None,
                "category": "smalltalk:goodbye"
            }
        
        best_faq, confidence = self.find_best_match(user_question)
        
        if best_faq:
            return {
                "answer": best_faq.answer,
                "confidence": round(confidence, 3),
                "matched_question": best_faq.question,
                "category": best_faq.category
            }
        else:
            return {
                "answer": "I'm sorry, I couldn't find a relevant answer to your question. Please try rephrasing it or contact support for assistance.",
                "confidence": round(confidence, 3),
                "matched_question": None,
                "category": None
            }

