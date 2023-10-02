import requests
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from textblob import TextBlob
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

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

# Se o texto foi baixado com sucesso, você pode realizar análise de sentimento e pré-processamento
if 'texto' in locals():
    # Realizar uma análise de sentimento
    blob = TextBlob(texto)
    sentiment = blob.sentiment

    # Exemplo de análise de sentimento
    # print("Polaridade do Sentimento:", sentiment.polarity)
    # print("Subjetividade do Texto:", sentiment.subjectivity)

    # Pré-processamento do texto (removendo caracteres especiais, por exemplo)
    texto = re.sub(r'[^\w\s]', '', texto)

    # Tokenização do texto
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([texto])
    sequences = tokenizer.texts_to_sequences([texto])
    
    # Converter as sequências em sequências com tamanho fixo (padding)
    MAX_SEQUENCE_LENGTH = 100  # Defina o tamanho máximo da sequência desejada
    padded_sequences = pad_sequences(sequences, maxlen=30)

    # Agora você pode usar as sequências padronizadas como entrada para a sua rede neural
    x = np.array(padded_sequences)  # Converter para um array NumPy
    y = np.array([sentiment.polarity])  # Converter a polaridade do sentimento para um array NumPy

    from keras.models import Sequential
    from keras.layers import Dense

    # Criando a arquitetura da rede neural 
    modelo = Sequential()
    modelo.add(Dense(units=3, activation='relu', input_dim=30))
    modelo.add(Dense(units=1, activation='linear'))

    # Treinando a rede neural
    modelo.compile(loss='mse', optimizer='adam', metrics=['mae'])

else:
    print("Não foi possível baixar o texto da URL.")

# Pré-processamento da pergunta
pergunta = "Qual é a opinião sobre o produto?"

# Pré-processamento da pergunta (usando o mesmo tokenizer e MAX_SEQUENCE_LENGTH do treinamento)
pergunta = re.sub(r'[^\w\s]', '', pergunta)
pergunta_sequences = tokenizer.texts_to_sequences([pergunta])
pergunta_padded = pad_sequences(pergunta_sequences, maxlen=30)

# Fazer a previsão com a rede neural
resposta = modelo.predict(pergunta_padded)

# Interpretar a resposta (exemplo fictício)
limite_positivo = 0.2  # Defina um limite adequado com base em suas previsões
if resposta > limite_positivo:
    resposta_final = "A opinião é positiva!"
else:
    resposta_final = "A opinião é neutra ou negativa."

# Apresentar a resposta ao usuário
print(resposta_final)