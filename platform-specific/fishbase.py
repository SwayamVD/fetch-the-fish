import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def fetch_fishbase_structured_by_class(species_name):
    url = f"https://www.fishbase.se/summary/{species_name}.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', id='ss-main')

    if not main_content:
        print("Could not find the main content div.")
        return

    sections = defaultdict(list)
    
    headings = main_content.find_all('h1', class_='slabel')

    for heading in headings:
        current_section = heading.get_text(strip=True)
        # Iterate through all siblings after heading
        for sibling in heading.find_next_siblings():
            # Stop if the next heading is found
            if sibling.name == 'h1' and 'slabel' in sibling.get('class', []):
                break
            # Check for p tags or div.smallSpace
            if (sibling.name == 'p' or (sibling.name == 'div' and 'smallSpace' in sibling.get('class', []))) \
                and sibling.get_text(strip=True):
                sections[current_section].append(sibling.get_text(strip=True))

    # Optional: print nicely
    for section_title, paragraphs in sections.items():
        print(f"\n{section_title.upper()}")
        for para in paragraphs:
            print(para)

    return sections

# Example usage
species_name = 'Acanthurus gahhm'
data = fetch_fishbase_structured_by_class(species_name)
