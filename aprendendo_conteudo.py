import requests
import re
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin

# URL da página inicial do site
base_url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Inicialize uma fila para armazenar todas as URLs a serem visitadas
url_queue = deque([base_url])

# Inicialize uma lista para armazenar todas as URLs já visitadas
visited_urls = set()

# Inicialize uma lista para armazenar todos os textos  coletados
collected_text = []

# Função para extrair links de uma página
def extract_links(url):
    links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                link = a['href']
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

# Inicie o processo de coleta de informações
while url_queue:
    url = url_queue.popleft()
    if url not in visited_urls:
        print(f"Visitando: {url}")
        visited_urls.add(url)
        collect_text(url)
        new_links = extract_links(url)
        url_queue.extend(new_links)

# Salvar os textos coletados em um arquivo
with open('textos_coletados.txt', 'w', encoding='utf-8') as file:
    for text in collected_text:
        file.write(text + '\n')