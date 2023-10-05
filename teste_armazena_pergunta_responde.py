import requests
import re
import spacy
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse, urljoin

# URL da página inicial do site
base_url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Inicialize uma fila para armazenar todas as URLs a serem visitadas
url_queue = deque([base_url])

# Inicialize uma lista para armazenar todas as URLs já visitadas
visited_urls = set()

# Função para extrair links de uma página
def extract_links(url):
    links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                link = a['href']
                # Verifique se o link é relativo e converta-o para uma URL absoluta
                parsed_link = urlparse(link)
                if not parsed_link.netloc:  # Link relativo
                    link = urljoin(base_url, link)
                links.append(link)
    except Exception as e:
        print(f"Erro ao extrair links de {url}: {e}")
    return links

# Função para visitar todas as URLs e coletar informações
def scrape_site(limit_urls=3):
    while url_queue and len(visited_urls) < limit_urls:
        url = url_queue.popleft()
        if url not in visited_urls:
            print(f"Visitando: {url}")
            visited_urls.add(url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    texto = response.text
                    # Pré-processamento do texto (removendo caracteres especiais, por exemplo)
                    texto = re.sub(r'[^\w\s]', '', texto)
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
                        # Lógica personalizada para encontrar respostas com base no texto processado
                        if "opinião" in pergunta and "produto" in pergunta:
                            resposta = "A opinião sobre o produto é positiva."
                        else:
                            resposta = "Desculpe, não tenho informações para essa pergunta."
                    # Apresentar a resposta ao usuário
                    print(resposta)
                else:
                    print(f"Erro ao baixar o arquivo. Status code: {response.status_code}")
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
            new_links = extract_links(url)
            url_queue.extend(new_links)

# Carregar o modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

# Inicie o processo de coleta de informações, limitando-se a 3 URLs
scrape_site(limit_urls=3)
