import spacy

# Carregar o modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

# Carregar os textos coletados a partir do arquivo
collected_text = []
with open('textos_coletados.txt', 'r', encoding='utf-8') as file:
    for line in file:
        collected_text.append(line.strip())

# Função para processar o texto e responder à pergunta
def process_text_and_question(text, pergunta):
    doc = nlp(text)
    # Encontrar entidades relevantes na pergunta
    entidades = [ent.text for ent in doc.ents]
    if len(entidades) > 0:
        resposta = "Desculpe, não tenho informações suficientes para responder a essa pergunta."
    else:
        if "opinião" in pergunta and "produto" in pergunta:
            resposta = "A opinião sobre o produto é positiva."
        else:
            resposta = "Desculpe, não tenho informações para essa pergunta."
    return resposta

# Pré-processamento da pergunta
pergunta = "O que você acha do produto?"

# Processar o texto coletado e responder à pergunta
for text in collected_text:
    resposta = process_text_and_question(text, pergunta)
    print(resposta)
