import requests
import time

# Функция для проверки домена на наличие вирусов
def check_domain_for_viruses(domain, api_key):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        stats = data['data']['attributes']['last_analysis_stats']
        if stats['malicious'] > 0 or stats['suspicious'] > 0:
            return f"{domain}: Потенциально опасен. Вредоносных: {stats['malicious']}, Подозрительных: {stats['suspicious']}\n"
        else:
            return f"{domain}: Безопасен.\n"
    else:
        return f"{domain}: Не удалось проверить.\n"

# Ваш API ключ
api_key = "cfc85e1270c90f08765facd3b004f85a2556043d317287fdf0e5a7bb006880f6"

# Чтение доменов из файла и проверка каждого
with open('domains.txt', 'r') as file:
    domains = file.readlines()

# Открытие файла output.txt для записи результатов
with open('output.txt', 'w') as output_file:
    for index, domain in enumerate(domains):
        domain = domain.strip()  # Удаление лишних пробелов и символов новой строки
        result = check_domain_for_viruses(domain, api_key)
        print(result, end='')  # Вывод результата в консоль
        output_file.write(result)  # Запись результата в файл
        if index != len(domains) - 1:
            time.sleep(15)  # Задержка на 15 секунд

print("Анализ завершен, результаты сохранены в output.txt.")
