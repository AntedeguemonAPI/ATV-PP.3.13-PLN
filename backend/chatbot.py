from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np
from spellchecker import SpellChecker
import spacy
import subprocess
import sys

try:
    spacy.load("pt_core_news_sm")
except OSError:
    print("Baixando modelo pt_core_news_sm do spaCy...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"])

class ChatBot:
    def __init__(self):
        self.questions = []
        self.answers = []
        # Carregar o modelo spaCy em português
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            print("Modelo spaCy 'pt_core_news_sm' não encontrado. "
                  "Faça o download com: python -m spacy download pt_core_news_sm")
            self.nlp = None

        # Inicializar o corretor ortográfico para português
        self.spell = SpellChecker(language='pt')

        self.vectorizer = TfidfVectorizer(tokenizer=self.custom_tokenizer)
        self.tfidf_matrix = None
        self.setup_base_knowledge()
    
    def custom_tokenizer(self, text):
        tokens = re.findall(r'\b\w+\b|\[PROGRAMA\]', text)
        return tokens

    def correct_text(self, text):
        # Corrige cada palavra, exceto [PROGRAMA] e a última palavra (possível nome do programa)
        words = text.split()
        corrected = []
        for i, word in enumerate(words):
            if word.upper() == "[PROGRAMA]":
                corrected.append("[PROGRAMA]")
            # Não corrige a última palavra (nome do programa)
            elif i == len(words) - 1:
                corrected.append(word)
            else:
                corrected.append(self.spell.correction(word) or word)
        return " ".join(corrected)

    def lemmatize_text(self, text):
        if not self.nlp:
            return text.lower()
        placeholder = "PROGRAM_PLACEHOLDER_XYZ"
        text_with_placeholder = text.replace("[PROGRAMA]", placeholder)
        doc = self.nlp(text_with_placeholder.lower())
        lemmatized_tokens = []
        for token in doc:
            if token.text == placeholder.lower():
                lemmatized_tokens.append("[PROGRAMA]")
            elif not token.is_stop and not token.is_punct and token.is_alpha:
                lemmatized_tokens.append(token.lemma_)
        return " ".join(lemmatized_tokens)

    def setup_base_knowledge(self):
        base_qa = [
            ("Como instalo um programa [PROGRAMA]",
             "Para instalar [PROGRAMA], siga estes passos:\n1. Baixe o instalador\n2. Execute o arquivo .exe\n3. Siga as instruções na tela\n4. Complete a instalação"),
            ("Preciso de ajuda com login",
             "Você pode redefinir sua senha na página de login clicando em 'Esqueci minha senha'."),
            ("Onde encontro configurações",
             "As configurações estão no canto superior direito, clique no ícone de engrenagem."),
            ("Como atualizo um software",
             "Para atualizar um software, vá em Configurações > Atualizações e clique em 'Verificar atualizações'."),
            ("sair", "Até logo! Espero ter ajudado."),
            ("quero sair", "Até mais! Volte sempre que precisar."),
            ("encerrar", "Encerrando a sessão. Tenha um bom dia!"),
            ("ajuda", "Posso ajudar com:\n- Instalação de programas\n- Problemas de login\n- Configurações do sistema\n- Atualizações de software")
        ]
        self.train(base_qa)
    
    def train(self, qa_pairs):
        self.questions = []
        self.answers = []
        for question, answer in qa_pairs:
            processed_q = self.process_question_patterns(question)
            lemmatized_q = self.lemmatize_text(processed_q)
            self.questions.append(lemmatized_q)
            self.answers.append(answer)
        if self.questions:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)
        else:
            self.tfidf_matrix = None

    def process_question_patterns(self, question):
        if "[PROGRAMA]" in question:
            parts = question.split("[PROGRAMA]")
            processed_parts = [p.lower() for p in parts]
            return "[PROGRAMA]".join(processed_parts)
        return question.lower()
    
    def get_response(self, user_input):
        # Garante que user_input é string
        if isinstance(user_input, dict):
            user_input = user_input.get('message', '')
        elif not isinstance(user_input, str):
            user_input = str(user_input)
        user_input_lower = user_input.lower()
        user_input_corrigido = self.correct_text(user_input_lower)
        lemmatized_user_input = self.lemmatize_text(user_input_corrigido)

        # Verifica se houve correção ortográfica
        if user_input_lower != user_input_corrigido:
            # Sugere a frase corrigida ao usuário
            sugestao = user_input_corrigido.capitalize()
            return {
                "resposta": f'Você quis dizer "{sugestao}"?',
                "correcao_sugerida": sugestao,
                "tipo": "confirmacao_correcao"
            }

        # Comandos de saída
        exit_keywords = ['sair', 'encerrar', 'quero sair', 'adeus']
        if any(keyword in lemmatized_user_input for keyword in exit_keywords):
            return {"resposta": "Até logo! Espero ter ajudado.", "tipo": "saida"}

        # Comando de ajuda
        if 'ajuda' in lemmatized_user_input:
            try:
                help_question_lemmatized = self.lemmatize_text(self.process_question_patterns("ajuda"))
                return {"resposta": self.answers[self.questions.index(help_question_lemmatized)], "tipo": "resposta"}
            except ValueError:
                return {"resposta": "Posso ajudar com instalação de programas, login, configurações e atualizações.", "tipo": "resposta"}

        # Pergunta sobre instalação de programa específico
        try:
            program_match = re.search(
                r'(?:como\s+(?:instalar|instala|faço\s+para\s+instalar)|instalar|instala)\s+(?:o\s+|um\s+)?([a-zA-Z0-9\s.-]+)',
                lemmatized_user_input
            )
            if program_match:
                program_name = program_match.group(1)
                if program_name:
                    program_name = program_name.strip()
                    try:
                        base_q_lemmatized = self.lemmatize_text(self.process_question_patterns("Como instalo um programa [PROGRAMA]"))
                        base_response_idx = self.questions.index(base_q_lemmatized)
                        base_response = self.answers[base_response_idx]
                        return {"resposta": base_response.replace("[PROGRAMA]", program_name), "tipo": "resposta"}
                    except ValueError:
                        return {"resposta": f"Para instalar {program_name}, geralmente você precisa baixar o instalador e seguir as instruções.", "tipo": "resposta"}
        except re.error:
            pass

        # Processamento geral com TF-IDF
        processed_input_for_tfidf = self.process_user_input(lemmatized_user_input)
        if self.tfidf_matrix is not None and self.tfidf_matrix.shape[0] > 0 and processed_input_for_tfidf.strip():
            user_tfidf = self.vectorizer.transform([processed_input_for_tfidf])
            similarities = cosine_similarity(user_tfidf, self.tfidf_matrix)
            if similarities.size > 0:
                most_similar_idx = np.argmax(similarities)
                similarity_threshold = 0.1
                if similarities[0, most_similar_idx] > similarity_threshold:
                    return {"resposta": self.answers[most_similar_idx], "tipo": "resposta"}
        return {"resposta": "Desculpe, não entendi completamente. Você poderia reformular? Por exemplo: 'Como instalo o Photoshop?' ou 'Preciso de ajuda com login'", "tipo": "resposta"}

    def process_user_input(self, lemmatized_text_input):
        normalized = re.sub(r'\b(instalar)\s+(?:o\s+|um\s+)?([a-zA-Z0-9\s.-]+)', r'instalar [PROGRAMA]', lemmatized_text_input)
        return normalized