import os
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import datetime
import shutil
import subprocess

# Function to read domains from file
def read_domains(file_path):
    with open(file_path, 'r') as file:
        return [domain.strip() for domain in file.readlines()]

# Function to write domains to file
def write_domains(domains, output_file):
    with open(output_file, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")

# Function to check for news related to domain
def check_domain_for_news(domain):
    base_url = "http://xmlriver.com/search/xml"
    params = {
        "setab": "news",
        "user": "8677",
        "key": "5b7e4d6a8fdc9130b39487dca999b99ba4fb1b08",
        "query": f"site:{domain}"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        xml_root = ElementTree.fromstring(response.content)
        return xml_root.find('.//results') is not None
    except (requests.RequestException, ElementTree.ParseError) as e:
        print(f"Error checking news for domain {domain}: {e}")
        return False

# Function to get first indexing date from Google
def get_first_indexing_date(domain):
    url = f'https://www.google.com/search?q=About+https://{domain}/&tbm=ilp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(attrs={"jsrenderer": "ndJhy"})
        for element in elements:
            if "Site first indexed by Google" in element.text:
                return element.text.replace("Site first indexed by Google", "").strip()
    except requests.RequestException as e:
        print(f"Error getting indexing date for domain {domain}: {e}")
    return None

# Function to find common domains
def find_common_domains(file1, file2):
    domains1 = set(read_domains(file1))
    domains2 = set(read_domains(file2))
    return list(domains1 & domains2)

def main():
    input_file = 'expiredDomains.txt'
    output_file_with_date = '1_OldImg.txt'
    output_file_with_news = '2_HaveNews.txt'
    common_domains_output_file = '3_both.txt'
    output_txt_file = 'output.txt'
    target_directory = r'B:\promma\SEO\HowOldSite\probeli'
    target_domains_file = os.path.join(target_directory, 'domains.txt')
    script_to_run = os.path.join(target_directory, 'script.py')

    # Delete output.txt if it exists
    if os.path.exists(output_txt_file):
        os.remove(output_txt_file)
        print(f"{output_txt_file} deleted.")

    domains = read_domains(input_file)
    total_domains = len(domains)
    domains_with_news = []
    domains_with_date = []
    domains_without_news = []

    print("Processing...")

    for index, domain in enumerate(domains):
        if not domain:
            continue
        
        if check_domain_for_news(domain):
            domains_with_news.append(domain)
            print(f"{domain} - Have News")
        else:
            domains_without_news.append(domain)
            print(f"{domain} - null")

        indexing_date = get_first_indexing_date(domain)
        if indexing_date:
            domains_with_date.append(domain)
            print(f"First indexing date found for {domain}: {indexing_date}")
        
        print(f"Processed {index + 1} of {total_domains}. Found {len(domains_with_news)} domains with news.")

    write_domains(domains_with_date, output_file_with_date)
    write_domains(domains_with_news, output_file_with_news)

    common_domains = find_common_domains(output_file_with_date, output_file_with_news)
    write_domains(common_domains, common_domains_output_file)
    write_domains(common_domains, output_txt_file)

    print(f"Total checked domains: {total_domains}")
    print(f"Domains with news: {len(domains_with_news)}")
    print(f"Common domains: {len(common_domains)}")

    # Move 3_both.txt to the target directory and overwrite domains.txt
    shutil.copy(common_domains_output_file, target_domains_file)
    print(f"Copied {common_domains_output_file} to {target_domains_file}")

    # Run script.py in the target directory
    try:
        subprocess.run(['python', script_to_run], check=True)
        print(f"Ran {script_to_run} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")

if __name__ == "__main__":
    main()
