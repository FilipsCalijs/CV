import requests
import re
from xml.etree import ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

def запрос_домена(domain):
    # Заменяем точку на пробел в домене
    отформатированный_домен = domain.replace('.', ' ')
    # Формируем URL запроса
    url = f"http://xmlriver.com/search/xml?user=8677&key=5b7e4d6a8fdc9130b39487dca999b99ba4fb1b08&query={отформатированный_домен}"
    # Отправляем запрос
    response = requests.get(url)
    # Возвращаем XML ответ
    return domain, response.text

def разобрать_xml_ответ(domain, xml_response):
    print(xml_response)  # Добавьте эту строку для отладки
    root = ET.fromstring(xml_response)
    найденные_ссылки = []
    # Перебираем каждый элемент <group> в ответе
    for group in root.findall('.//group'):
        group_id = group.get('id')  # Получаем id группы
        for doc in group.findall('.//doc'):
            url = doc.find('url').text
            # Формируем правильный шаблон для сравнения
            шаблон_домена = f"https?://(www.)?{domain}/?"
            # Проверяем, соответствует ли URL шаблону
            if re.match(шаблон_домена, url):
                # Добавляем URL и group_id в список найденных ссылок
                найденные_ссылки.append((url, group_id))
    return найденные_ссылки

def обработать_домен(domain, итоговые_результаты):
    domain, xml_response = запрос_домена(domain)
    найденные_ссылки = разобрать_xml_ответ(domain, xml_response)
    
    # Сохраняем результаты в файл сразу после получения ответа
    with open('output.txt', 'a') as file:
        for url, group_id in найденные_ссылки:
            file.write(f"{url};{group_id}\n")
    
    # Добавляем результаты в общий список для статистики
    итоговые_результаты.extend(найденные_ссылки)
    
    return domain, найденные_ссылки

def main():
    итоговые_результаты = []
    # Читаем домены из файла
    with open('domains.txt', 'r') as file:
        домены = file.read().splitlines()
    
    всего_доменов = len(домены)
    проверено_доменов = 0
    
    # Используем ThreadPoolExecutor для многопоточности
    with ThreadPoolExecutor(max_workers=10) as executor:
        результаты = list(executor.map(lambda domain: обработать_домен(domain, итоговые_результаты), домены))
    
    for domain, найденные_ссылки in результаты:
        проверено_доменов += 1
        оставшиеся_домены = всего_доменов - проверено_доменов
        
        # Выводим информацию о прогрессе и результатах
        print(f"Проверено доменов: {проверено_доменов} из {всего_доменов}, осталось проверить: {оставшиеся_домены}")
        
        if найденные_ссылки:
            for url, group_id in найденные_ссылки:
                print(f"Найденный URL для {domain}: {url}; Group ID: {group_id}")
        else:
            print(f"Для домена {domain} подходящих результатов не найдено.")
    
    print(f"Всего найдено результатов: {len(итоговые_результаты)}")

if __name__ == "__main__":
    main()
