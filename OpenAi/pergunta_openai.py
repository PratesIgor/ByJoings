import openai

# Chave da API do GPT-3 (substitua pela sua chave)
api_key = "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"

# Inicialize o cliente do GPT-3
openai.api_key = api_key

# Função para consultar o GPT-3 com uma pergunta e um texto coletado
def consultar_gpt3(texto, pergunta):
    # Use o GPT-3 para gerar uma resposta com base na pergunta e no texto coletado
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Texto: {texto}\nPergunta: {pergunta}\nResposta:",
        max_tokens=50  # Ajuste o número de tokens máximo conforme necessário
    )

    # Obtenha a resposta do GPT-3
    resposta = response.choices[0].text.strip()

    return resposta

# Ler as URLs coletadas a partir do arquivo
with open('urls_coletadas.txt', 'r') as file:
    urls_coletadas = file.read().splitlines()

# Pergunta que você deseja fazer para cada URL
pergunta = input("Como eu posso te ajudar hoje?")

# Consultar o GPT-3 para cada URL e exibir as respostas
for url in urls_coletadas:
    resposta = consultar_gpt3(url, pergunta)
    print(f"Pergunta para URL {url}:\n{pergunta}\nResposta:\n{resposta}\n")
