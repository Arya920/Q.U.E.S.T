import requests
from bs4 import BeautifulSoup

def search_google(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    snippet = ""
    for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
        if len(g.text.split()) > 5: 
            snippet = g.text
            break
    
    words = snippet.split()
    words = ' '.join(words[:50])
    return words
