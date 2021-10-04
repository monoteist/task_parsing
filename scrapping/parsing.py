import asyncio
from pprint import pprint
from random import choice
from bs4 import BeautifulSoup as bs
from aiohttp import ClientSession
import json
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(run(links))
    data_links = loop.run_until_complete(future)
    data = {link: d for link, d in zip(links, data_links)}
    return tuple(data.items())

async def run(links):
    async with ClientSession() as session:
        tasks = []
        for link in links:
            href = f'https://api.domainsdb.info/v1/domains/search?domain={link}'
            task = async_req(href, session)
            tasks.append(task)
        return await asyncio.gather(*tasks)

async def async_req(href, session):
    async with session.get(href) as response:
        return await response.json()
