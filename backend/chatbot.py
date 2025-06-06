from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ChatBot:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.vectorizer = CountVectorizer()
        self.bow_matrix = None
    
    def train(self, qa_pairs):
        """Train the chatbot with question-answer pairs"""
        self.questions = [pair[0].lower() for pair in qa_pairs]
        self.answers = [pair[1] for pair in qa_pairs]
        
        # Create Bag of Words model
        self.bow_matrix = self.vectorizer.fit_transform(self.questions)
    
    def get_response(self, user_input):
        """Get response for user input"""
        user_input = user_input.lower()
        
        # Check for exit commands
        if any(word in user_input for word in ['sair', 'encerrar', 'quero sair']):
            return self.answers[self.questions.index('sair')]
        
        # Transform user input to BoW
        user_bow = self.vectorizer.transform([user_input])
        
        # Calculate similarity with trained questions
        similarities = cosine_similarity(user_bow, self.bow_matrix)
        most_similar_idx = np.argmax(similarities)
        
        # Threshold for similarity (adjust as needed)
        if similarities[0, most_similar_idx] > 0.5:
            return self.answers[most_similar_idx]
        else:
            return "Desculpe, não entendi. Você pode reformular sua pergunta?"