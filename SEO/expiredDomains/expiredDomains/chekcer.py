import os
import requests
from xml.etree import ElementTree
import datetime

# Функция для чтения доменов из файла
def read_domains(file_path):
    with open(file_path, 'r') as file:
        domains = file.readlines()
    return [domain.strip() for domain in domains]

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
            if xml_root.find('.//results') is not None:
                return True
            else:
                return False
        except ElementTree.ParseError:
            return False
    else:
        return False

def main():
    input_file = r'B:\promma\SEO\HowOldSite\expiredDomains\expiredDomains.txt'
    output_file_with_news = r'B:\promma\SEO\HowOldSite\expiredDomains\have_news.txt'
    output_txt_file = 'output.txt'

    # Чтение доменов из файла
    domains = read_domains(input_file)

    print("Идет загрузка...")

    total_domains = len(domains)
    domains_with_news = 0
    domains_without_news = []

    # Получаем текущую дату для имени файла
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    with open(output_file_with_news, 'w') as output_file_news:
        for index, domain in enumerate(domains):
            if domain and domain not in domains_without_news:
                if check_domain_for_news(domain):
                    domains_with_news += 1
                    output_file_news.write(f"{domain}\n")
                    print(f"{domain} - Have News")
                else:
                    domains_without_news.append(domain)
                    print(f"{domain} - null")

            # Выводим информацию о прогрессе обработки
            print(f"Обработано {index + 1} из {total_domains}. Найдено {domains_with_news} доменов с новостями.")

    print(f"Общее количество проверенных доменов: {total_domains}")
    print(f"Количество доменов с новостями: {domains_with_news}")

    # Чтение доменов с новостями для записи в output.txt
    domains_for_output_txt = read_domains(output_file_with_news)
    with open(output_txt_file, 'w') as file:
        for domain in domains_for_output_txt:
            file.write(f"{domain}\n")

if __name__ == "__main__":
    main()
