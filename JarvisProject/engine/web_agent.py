import requests
from bs4 import BeautifulSoup
import ollama

def research_topic(topic):
    search_url = f"https://www.google.com/search?q={topic}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    snippets = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    context = " ".join([s.text for s in snippets[:3]])

    summary = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': f"Summarize this info about {topic}: {context}"}
    ])
    return summary['message']['content']