import requests
from bs4 import BeautifulSoup
import json

def fetch_quotes(page_no):
    url = f'https://quotes.toscrape.com/page/{page_no}/'
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []
    quote_elements = soup.find_all('div', class_='quote')

    for quote_text in quote_elements:
        quote = quote_text.find('span', class_='text').text
        author = quote_text.find('small', class_='author').text
        author_link = quote_text.find('a')['href']
        keywords = quote_text.find('meta', class_='keywords')['content'].split(',')
        tag_dict = []

        for keyword in keywords:
            tag_link = f'https://quotes.toscrape.com/tag/{keyword}/page/{page_no}/'
            tag_dict.append(tag_link)
        
        quotes.append({
            'quote': quote,
            'author': author,
            'author_link': f'https://quotes.toscrape.com/{author_link}',
            'keywords': keywords,
            'tag_links': tag_dict,
        });
    
    return quotes
  
def main():
    all_quotes = []
    max_pages = 10
  
    for current_page in range(1, max_pages + 1):
        quotes_on_page = fetch_quotes(current_page)
        all_quotes.extend(quotes_on_page)
        
    with open('quotes.json', 'w') as f:
        json.dump(all_quotes, f, indent=2)
    print('Quotes saved to quotes.json file')

if __name__ == "__main__":
    main()
