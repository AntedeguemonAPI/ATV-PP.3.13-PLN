# ATV-PP.3.13-PLN

Repositório destinado à Atividade PP.3.13 da disciplina de PLN.

## Enunciado do Exercício

Desenvolva um chatbot simples capaz de responder perguntas sobre instalação de programas, problemas de login, configurações e atualizações de software. O chatbot deve ser capaz de:

- Corrigir erros ortográficos comuns na entrada do usuário.
- Sugerir correções quando identificar palavras digitadas incorretamente.
- Reconhecer comandos como "sair", "ajuda", "como instalar [programa]", entre outros.
- Utilizar técnicas de PLN como lematização e TF-IDF para identificar a intenção do usuário.
- Ser acessível por uma interface web simples.

## Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/AntedeguemonAPI/ATV-PP.3.13-PLN.git
cd ATV-PP.3.13-PLN
```

### 2. Instale as dependências

No diretório `backend`:

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # No Windows
# source venv/bin/activate  # No Linux/Mac

pip install -r requirements.txt
```

### 3. Baixe o modelo do spaCy para português

```bash
python -m spacy download pt_core_news_sm
```

### 4. Rode o backend Flask

```bash
python app.py
```

### 5. Acesse o frontend

Abra o arquivo `frontend/index.html` no navegador  
**ou** acesse `http://localhost:5000` se o backend estiver rodando.

---

**Observação:**  
Se for rodar em outro ambiente, garanta que as portas não estejam bloqueadas e que o modelo do spaCy esteja instalado.

---

## Equipe do Projeto

|    Função     | Nome                           |                                                                                                                                                    LinkedIn & GitHub                                                                                                                                                     |
| :-----------: | :----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|   Dev Team    | Thiago Frederico da Silva Zani |        [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/thiago-zani-1b8503249/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/zani19)        |
|   Dev Team    | Jean Lucas de Faria Silva      |              [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/jeanlfs/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/jeejinf)               |
|   Dev Team    | Gabriel Brosig Briscese        | [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-brosig-briscese-344a5587/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Briscese)  |
| Scrum Master  | Jonatas Mathias Dalló          |   [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/jonatas-mathias-147638206) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Jonatas-Dallo)   |
| Product Owner | Miguel Carvalho Soares         | [![Linkedin Badge](https://img.shields.io/badge/Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/miguel-carvalho-soares-722b161a3/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Miguel-C1) |
