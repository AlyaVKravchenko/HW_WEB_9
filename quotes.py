import requests
from bs4 import BeautifulSoup
import json
from models import Author, Quote


# Function to scrape quotes from a page
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []

    for quote_elem in soup.select('div.quote'):
        text = quote_elem.select_one('span.text').get_text(strip=True)
        author_name = quote_elem.select_one('small.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_elem.select('div.tags a')]

        quotes.append({
            'text': text,
            'author': author_name,
            'tags': tags
        })

    return quotes


# Function to scrape authors from a page
def scrape_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    authors = []

    for author_elem in soup.select('div.author'):
        name = author_elem.select_one('h3.author-title').get_text(strip=True)
        birthdate = author_elem.select_one('span.author-born-date').get_text(strip=True)
        birthplace = author_elem.select_one('span.author-born-location').get_text(strip=True)
        bio = author_elem.find_next('div', class_='author-description').get_text(strip=True)

        authors.append({
            'fullname': name,
            'born_date': birthdate,
            'born_location': birthplace,
            'description': bio
        })

    return authors


# URL of the website
base_url = 'http://quotes.toscrape.com'
quotes_url = f'{base_url}/page/1/'
authors_url = f'{base_url}/authors/'

# Scrape quotes from all pages
all_quotes = []
page_number = 1

while quotes_url:
    quotes = scrape_quotes(quotes_url)
    all_quotes.extend(quotes)
    page_number += 1
    quotes_url = f'{base_url}/page/{page_number}/' if f'/page/{page_number}/' in requests.get(quotes_url).text else None

# Scrape authors
all_authors = scrape_authors(authors_url)

# Save quotes to quotes.json
with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(all_quotes, quotes_file, ensure_ascii=False, indent=2)

# Save authors to authors.json
with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(all_authors, authors_file, ensure_ascii=False, indent=2)