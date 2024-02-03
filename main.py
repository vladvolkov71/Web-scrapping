import json
import re
from pprint import pprint
import bs4
import fake_headers
import requests

URL = "https://hh.ru/search/vacancy?text=Python+django+flask&search_field=description&enable_snippets=true&area=1&area=2"


def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()


response = requests.get(URL, headers=gen_headers())
main_html = response.text
main_page = bs4.BeautifulSoup(main_html, "lxml")

vacancy_list_tag = main_page.find("div", id="a11y-main-content")
vacncies_tags = vacancy_list_tag.find_all("div", class_="serp-item")
vacancies_data = []
for vacancy_tag in vacncies_tags:
    v_name_tag = vacancy_tag.find("span", class_="serp-item__title")  # название вакансии
    v_name = v_name_tag.text.strip()
    v_link = vacancy_tag.find("a")["href"]  # ссылка на вакансию

    v_compensation_tag = vacancy_tag.find("span", class_="bloko-header-section-2")  # зарплата
    v_compensation = (
        re.sub('\u202f', '', v_compensation_tag.text.strip()) if v_compensation_tag else "зарплата не указана"
    )
    v_employer_tag = vacancy_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")  # организация

    v_employer = (
        re.sub('\xa0', ' ', v_employer_tag.text.strip()) if v_employer_tag else "не указана"
    )
    v_address_tag = vacancy_tag.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"})  # город
    v_address = (
        re.findall(r'^\w+-*\w*\b', v_address_tag.text.strip())[0] if v_address_tag else "город не указан"
    )
    # if re.search(r'\$', v_compensation): # проверка на зарплату в долларах

    vacancies_data.append(
        {
            "name": v_name,  # название вакансии
            "link": v_link,  # ссылка на вакансию
            "compensation": v_compensation,  # зарплата
            "employer": v_employer,  # организация
            "address": v_address,  # город
        }
    )

pprint(vacancies_data, width=100, sort_dicts=False)

with open("vacancies_data.json", "w", encoding="utf-8") as file:
    json.dump(vacancies_data, file, indent=4, ensure_ascii=False)
