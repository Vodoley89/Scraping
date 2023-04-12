import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json
from unicodedata import normalize

ITEMS = 100
URL = f'https://spb.hh.ru/search/vacancy?area=2&area=1&&search_field=name&currency_code=USD&text=python&items_on_page={ITEMS}'
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Coonection': 'keep-alive'
}
word = "text=python+django+flask"
dict_jobs = {}
jobs = []


hh_r = requests.get(URL, headers=headers)  # Запрос на получение ссылки
hh_soup = BeautifulSoup(hh_r.text, 'lxml')

pages = []
paginator = hh_soup.find_all('span', {'class': "pager-item-not-in-short-range"})

for page in paginator:
    pages.append(int(page.find('a').text))




result = requests.get(f'{URL}&page=0', headers=headers)
soup = BeautifulSoup(result.text, 'lxml')
results = soup.find_all('div', class_='serp-item')

for result in results:
    job = result.find('a')
    job2 = result.find('a').text
    links = f"{job['href']}{word}"

    company = result.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    salary = 'з/п не указана'
    if result.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"}):
        salary = result.find('span', attrs={"data-qa": "vacancy-serp__vacancy-compensation"}).get_text()
    city = result.find('div', attrs={"data-qa": "vacancy-serp__vacancy-address"}).text


    jobs.append({job2: {'link': normalize('NFKD', links),
                        'company': normalize('NFKD', company),
                        'salary': normalize('NFKD', salary),
                        'city': normalize('NFKD', city)}})


with open ('jobs.json', 'w', encoding='utf-8') as file:
    json.dump(jobs, file, ensure_ascii=False)

