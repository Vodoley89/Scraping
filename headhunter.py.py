#Домашнее задание к лекции 6.«Web-scrapping»
# Попробуем получать интересующие вакансии на сайте headhunter самыми первыми :)
#
# 1) Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург".
# Эти параметры задаются по ссылке
# 2) Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
# 3) Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.



import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json

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
dict = {}


# def get_max_page():
hh_r = requests.get(URL, headers=headers)                   # Запрос на получение ссылки
hh_soup = BeautifulSoup(hh_r.text, 'lxml')

pages = []
paginator = hh_soup.find_all('span', {'class': "pager-item-not-in-short-range"})        # Поиск элементов страниц

for page in paginator:
    pages.append(int(page.find('a').text))      # Получение ссылки на каждую страницу

    # return pages[-1]

# max_page = get_max_page()
# def exctract_hh_jobs(last_page):
jobs = []
    # for page in range(max_page):
result = requests.get(f'{URL}&page=0',headers=headers)
soup = BeautifulSoup(result.text, 'lxml')
            # print(result.status_code)
results = soup.find_all('div', class_='serp-item')


for result in results:
    job = result.find('a')
    links = f"{job['href']}{word}"
    company = result.find('a', class_= 'bloko-link bloko-link_kind-tertiary').text
    salary = result.find('span', attrs = {"data-qa": "vacancy-serp__vacancy-compensation"})
    city = result.find('div', attrs = {"data-qa": "vacancy-serp__vacancy-address"}).text
    # re_city = re.findall(r'\"(\w*)|(\w*\-\w*)\"', city, flags=re.MULTILINE)
    jobs.append({ job.text :
        {'link': links,
        'company': company,
        'salary': salary,
        'city': city,
    }})


json.dumps(jobs)