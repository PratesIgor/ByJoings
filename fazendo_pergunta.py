import requests
import pandas as pd
import numpy as np
import warnings
import re
import spacy

# URL da página da qual você deseja baixar texto
url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Baixar o conteúdo da URL usando o requests
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Ler o conteúdo da resposta HTTP como texto
    texto = response.text
else:
    print("Erro ao baixar o arquivo. Status code:", response.status_code)

# Se o texto foi baixado com sucesso, você pode realizar pré-processamento
if 'texto' in locals():
    # Pré-processamento do texto (removendo caracteres especiais, por exemplo)
    texto = re.sub(r'[^\w\s]', '', texto)

    # Carregar o modelo do spaCy
    nlp = spacy.load("pt_core_news_sm")

    # Processar o texto com o spaCy
    doc = nlp(texto)

    # Pré-processamento da pergunta
    pergunta = "Qual é a opinião sobre o produto?"

    # Encontrar entidades relevantes na pergunta
    entidades = [ent.text for ent in doc.ents]

    # Verificar se há entidades relevantes na pergunta
    if len(entidades) > 0:
        resposta = "Desculpe, não tenho informações suficientes para responder a essa pergunta."
    else:
        # Você pode usar lógica personalizada para encontrar respostas com base no texto processado
        # Neste exemplo, estamos procurando palavras-chave na pergunta
        if "opinião" in pergunta and "produto" in pergunta:
            resposta = "A opinião sobre o produto é positiva."
        else:
            resposta = "Desculpe, não tenho informações para essa pergunta."

    # Apresentar a resposta ao usuário
    print(resposta)
else:
    print("Não foi possível baixar o texto da URL.")
