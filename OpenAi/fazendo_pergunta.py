import requests
import re
import spacy
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin  # Importe urljoin para lidar com URLs relativas

# URL da página inicial do site
base_url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Inicialize uma fila para armazenar todas as URLs a serem visitadas
url_queue = deque([base_url])

# Inicialize uma lista para armazenar todas as URLs já visitadas
visited_urls = set()

# Inicialize uma lista para armazenar todos os textos coletados
collected_text = []

# Carregar o modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

# Função para extrair links de uma página
def extract_links(url):
    links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                link = a['href']
                # Use urljoin para lidar com URLs relativas
                absolute_link = urljoin(base_url, link)
                links.append(absolute_link)
    except Exception as e:
        print(f"Erro ao extrair links de {url}: {e}")
    return links

# Função para coletar texto de uma página
def collect_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            texto = response.text
            # Pré-processamento do texto (removendo caracteres especiais, por exemplo)
            texto = re.sub(r'[^\w\s]', '', texto)
            collected_text.append(texto)
    except Exception as e:
        print(f"Erro ao coletar texto de {url}: {e}")

# Função para processar o texto e responder à pergunta
def process_text_and_question(text, pergunta):
    # Processar o texto com o spaCy
    doc = nlp(text)
    # Encontrar entidades relevantes na pergunta
    entidades = [ent.text for ent in doc.ents]
    # Verificar se há entidades relevantes na pergunta
    if len(entidades) > 0:
        resposta = "Desculpe, não tenho informações suficientes para responder a essa pergunta."
    else:
        # Lógica personalizada para encontrar respostas com base no texto processado
        if "opinião" in pergunta and "produto" in pergunta:
            resposta = "A opinião sobre o produto é positiva."
        else:
            resposta = "Desculpe, não tenho informações para essa pergunta."
    return resposta

# Inicie o processo de coleta de informações
while url_queue:
    url = url_queue.popleft()
    if url not in visited_urls:
        print(f"Visitando: {url}")
        visited_urls.add(url)
        collect_text(url)
        new_links = extract_links(url)
        url_queue.extend(new_links)

# Pré-processamento da pergunta
pergunta = "Qual é a opinião sobre o produto?"

# Processar o texto coletado e responder à pergunta
for text in collected_text:
    resposta = process_text_and_question(text, pergunta)
    print(resposta)
