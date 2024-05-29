import requests
import re
from xml.etree import ElementTree as ET

def query_domain(domain):
    # Replace dot with space in the domain
    formatted_domain = domain.replace('.', ' ')
    # Form the query URL
    url = f"http://xmlriver.com/search/xml?user=8677&key=5b7e4d6a8fdc9130b39487dca999b99ba4fb1b08&query={formatted_domain}"
    # Send the request
    response = requests.get(url)
    # Return the XML response
    return response.text

def parse_xml_response(xml_response, domain):
    print(xml_response)  # Debugging line
    root = ET.fromstring(xml_response)
    found_urls = []
    # Check for errors in the response
    error = root.find('.//error')
    if error is not None:
        error_code = error.get('code')
        error_message = error.text
        print(f"Error code {error_code}: {error_message}")
        return found_urls
    
    # Iterate over each <group> element in the response
    for group in root.findall('.//group'):
        group_id = group.get('id')  # Get the group id
        for doc in group.findall('.//doc'):
            url = doc.find('url').text
            # Form the correct pattern for comparison
            domain_pattern = f"https?://(www.)?{domain}/?"
            # Check if the URL matches the pattern
            if re.match(domain_pattern, url):
                # Add the URL and group_id to the list of found URLs
                found_urls.append((url, group_id))
    return found_urls

def main():
    output_results = []
    # Read domains from the file
    with open('domains.txt', 'r') as file:
        domains = file.read().splitlines()
    
    for domain in domains:
        xml_response = query_domain(domain)
        found_urls = parse_xml_response(xml_response, domain)
        output_results.extend(found_urls)
        
        # Check if suitable URLs were found
        if found_urls:
            for url, group_id in found_urls:
                print(f"Found URL for {domain}: {url}; Group ID: {group_id}")
        else:
            print(f"No suitable results found for {domain}.")
    
    # Save results to a file
    with open('output.txt', 'w') as file:
        for url, group_id in output_results:
            file.write(f"{url};{group_id}\n")
    
    print(f"Total results found: {len(output_results)}")

if __name__ == "__main__":
    main()
