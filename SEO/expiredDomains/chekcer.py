import os
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import datetime
import re

# Функция для чтения доменов из файла
def read_domains(file_path):
    with open(file_path, 'r') as file:
        domains = file.readlines()
    return [domain.strip() for domain in domains]

# Функция для записи доменов с датой первой индексации в файл
def write_domains_with_date(domains, output_file):
    with open(output_file, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")

# Функция для записи доменов с новостями в файл
def write_domains_with_news(domains, output_file):
    with open(output_file, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")

# Функция для проверки наличия новостей по домену
def check_domain_for_news(domain):
    base_url = "http://xmlriver.com/search/xml"
    params = {
        "setab": "news",
        "user": "8677",
        "key": "5b7e4d6a8fdc9130b39487dca999b99ba4fb1b08",
        "query": f"site:{domain}"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        try:
            xml_root = ElementTree.fromstring(response.content)
            # Проверяем, есть ли элемент <results> в XML
            if xml_root.find('.//results') is not None:
                return True
            else:
                return False
        except ElementTree.ParseError:
            return False
    else:
        return False

# Функция для поиска общих доменов
def find_common_domains(file1, file2):
    domains1 = read_domains(file1)
    domains2 = read_domains(file2)
    
    common_domains = set(domains1) & set(domains2)
    return common_domains

# Функция для записи общих доменов в файл
def write_common_domains(domains, output_file):
    with open(output_file, 'w') as file:  
        for domain in domains:
            file.write(f"{domain}\n")

def main():
    input_file = r'B:\promma\SEO\HowOldSite\expiredDomains\expiredDomains.txt'
    output_file_with_date = r'B:\promma\SEO\HowOldSite\expiredDomains\how_old_Img_ended.txt'
    output_file_with_news = r'B:\promma\SEO\HowOldSite\expiredDomains\have_news.txt'
    common_domains_output_file = r'B:\promma\SEO\HowOldSite\expiredDomains\both.txt'
    output_txt_file = 'output.txt'

    # Определяем переменные для файлов вывода
    output_file_with_date = r'B:\promma\SEO\HowOldSite\expiredDomains\how_old_Img_ended.txt'
    output_file_with_news = r'B:\promma\SEO\HowOldSite\expiredDomains\have_news.txt'
    common_domains_output_file = r'B:\promma\SEO\HowOldSite\expiredDomains\both.txt'

    # Чтение доменов из файла
    domains = read_domains(input_file)

    print("Идет загрузка...")

    total_domains = len(domains)
    domains_with_date = 0
    domains_with_news = 0
    domains_without_news = []

    # Получаем текущую дату для имени файла
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Открываем файл для записи результатов
    with open(output_file_with_date, 'w') as output_file_date, open(output_file_with_news, 'w') as output_file_news:
        for index, domain in enumerate(domains):
            if domain:  # Проверяем, не пустая ли строка
                # Проверяем наличие новостей по домену только если домен еще не был добавлен в список без новостей
                if domain not in domains_without_news:
                    if check_domain_for_news(domain):
                        domains_with_news += 1
                        output_file_news.write(f"{domain}\n")
                        print(f"{domain} - Have News")
                    else:
                        domains_without_news.append(domain)
                        print(f"{domain} - null")

                url = f'https://www.google.com/search?q=About+https://{domain}/&tbm=ilp'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    elements = soup.find_all(attrs={"jsrenderer": "ndJhy"})
                    element_age = ""
                    for element in elements:
                        date_element = element.text
                        element_age = date_element.replace("Site first indexed by Google", "")
                    if element_age:
                        domains_with_date += 1
                        # Записываем домен в файл
                        output_file_date.write(f"{domain}\n")
                        print(f"Найдена дата первой индексации для {domain}: {element_age.strip()}")
                else:
                    print(f"Ошибка при загрузке страницы для домена {domain}")

                # Выводим информацию о прогрессе обработки
                print(f"Обработано {index + 1} из {total_domains}. Найдено {domains_with_news} доменов с новостями.")

    print(f"Общее количество проверенных доменов: {total_domains}")
    print(f"Количество доменов с новостями: {domains_with_news}")

    # Поиск общих доменов
    common_domains = find_common_domains(output_file_with_date, output_file_with_news)

    if common_domains:
        print("Найдены общие домены:")
        for domain in common_domains:
            print(domain)
        write_common_domains(common_domains, common_domains_output_file)
        print(f"Общие домены добавлены в файл: {common_domains_output_file}")

        # Теперь берем домены только из common_domains_output_file для записи в output.txt
        domains_for_output_txt = read_domains(common_domains_output_file)
        with open(output_txt_file, 'w') as file:
            for domain in domains_for_output_txt:
                file.write(f"{domain}\n")

    else:
        print("Общих доменов не найдено.")

if __name__ == "__main__":
    main()
