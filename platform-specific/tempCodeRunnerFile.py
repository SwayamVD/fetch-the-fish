import requests
from bs4 import BeautifulSoup

def fetch_fishbase_summary(species_name):
    url = f"https://www.fishbase.se/summary/{species_name}.html"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    small_spaces = soup.select('#ss-main .smallSpace')

    for i, div in enumerate(small_spaces, start=1):
        print(f"Element {i}: {div.get_text(strip=True)}")
    # # print(soup)
    # sections = soup.find_all("h1", class_="slabel bottomBorder")
    # for sec in sections:
    #     print(sec.get_text(strip=True))


# Example usage
species_name = 'Acanthurus gahhm'  # Replace with your species
fetch_fishbase_summary(species_name)

