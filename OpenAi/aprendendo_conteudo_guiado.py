import requests # Biblioteca para fazer solicitações HTTP
import re # Módulo para expressões regulares (usado para processamento de texto)
import spacy # Biblioteca de Processamento de Linguagem Natural (NLP)
from bs4 import BeautifulSoup # Biblioteca para fazer parsing de páginas HTML
from collections import deque # Módulo para criar uma fila de URLs a serem visitadas
from urllib.parse import urlparse, urljoin # Módulo para análise de URLs

from 

# URL da página inicial do site
base_url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Inicialize uma fila para armazenar todas as URLs a serem visitadas
url_queue = deque([base_url])

# Inicialize uma lista para armazenar todas as URLs já visitadas
visited_urls = set()

# Inicialize uma lista para armazenar as informações aprendidas
learned_information = []

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
def scrape_site():
    while url_queue:
        url = url_queue.popleft()
        if "/central-de-ajuda-avec" in url:  # Verifique se a URL contém "/central-de-ajuda-avec"
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
                        # Lógica personalizada para encontrar informações relevantes e aprendizado
                        # Por exemplo, você pode extrair informações de interesse aqui
                        # No exemplo a seguir, estamos apenas coletando o texto bruto da página
                        learned_information.append(texto)
                    else:
                        print(f"Erro ao baixar o arquivo. Status code: {response.status_code}")
                except Exception as e:
                    print(f"Erro ao processar {url}: {e}")
                new_links = extract_links(url)
                url_queue.extend(new_links)

# Carregar o modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

# Inicie o processo de coleta de informações
scrape_site()

# Após a conclusão, salve as informações aprendidas em um arquivo
with open('textos_coletados.txt', 'w', encoding='utf-8') as file:
    for info in learned_information:
        file.write(info + '\n')
