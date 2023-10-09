import requests
from bs4 import BeautifulSoup

# URL da página inicial do site
base_url = 'https://sites.google.com/hyperlocal.com.br/central-de-ajuda-avec'

# Faça uma solicitação HTTP para a página inicial
response = requests.get(base_url)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Obtenha o conteúdo da página
    page_content = response.text
    # Use BeautifulSoup p ara analisar o HTML
    soup = BeautifulSoup(page_content, 'html.parser')
    # Encontre todos os links na página
    links = soup.find_all('a', href=True)
    # Filtrar apenas os links para subpáginas do site
    subpage_urls = [link['href'] for link in links if '/central-de-ajuda-avec' in link['href']]
    # Construa URLs absolutas a partir dos links relativos
    subpage_urls = [base_url + url if not url.startswith('http') else url for url in subpage_urls]
    # Exiba a lista de URLs das subpáginas
    for url in subpage_urls:
        print(url)
else:
    print("Erro ao baixar o arquivo. Status code:", response.status_code)

# Após a conclusão, salve as informações aprendidas em um arquivo
with open('urls_coletadas.txt', 'w') as file:
    for url in subpage_urls:
        file.write(url + '\n')

print("URLs coletadas foram salvas em 'urls_coletadas.txt'.")