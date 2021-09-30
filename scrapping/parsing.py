from random import choice
import json
from bs4 import BeautifulSoup as bs
import requests

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def search_links(url):
    res = requests.get(url, headers=choice(headers))
    if res.status_code == 200:
        soup = bs(res.content, 'html.parser')
        a_list = soup.find_all('a')
        links = []
        for a in a_list:
            links.append(a['href'])
        return links
    return '404 not found'


def result(url):
    links = search_links(url)
    data = {}
    for link in links:
        href = f'https://api.domainsdb.info/v1/domains/search?domain={link}'
        res = requests.get(href).json()
        data.setdefault(link, res.get('domains'))
    return data
