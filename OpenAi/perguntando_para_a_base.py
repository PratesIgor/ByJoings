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
    # Aqui você pode implementar uma lógica mais avançada para responder à pergunta
    # Por exemplo, procurar palavras-chave na pergunta e no texto e gerar uma resposta com base nisso
    # Esta é apenas uma resposta de exemplo
    resposta = "Desculpe, não tenho informações suficientes para responder a essa pergunta."
    return resposta

# Fazer uma pergunta
pergunta = input("Faça sua pergunta: ")

# Processar o texto coletado e responder à pergunta
for text in collected_text:
    resposta = process_text_and_question(text, pergunta)
    # Apresentar a resposta ao usuário
    print(resposta)
