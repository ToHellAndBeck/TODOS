import requests
from bs4 import BeautifulSoup

def fetch_drudge_report_headlines():
    url = 'https://www.drudgereport.com'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.find_all('a', href=True):
        if len(headlines) >= 10:
            break
        text = item.get_text(strip=True)
        if text:
            headlines.append(text)
    
    return headlines

if __name__ == "__main__":
    headlines = fetch_drudge_report_headlines()
    for idx, headline in enumerate(headlines, 1):
        print(f"{idx}. {headline}")

