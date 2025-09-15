import requests
import json
def fetch_species_data(scientific_name):
    """
    Fetch species metadata from GBIF Species API based on scientific name.

    Args:
        scientific_name (str): The name of the species to search for.

    Returns:
        dict: JSON response from GBIF API, or error info.
    """
    url = "https://api.gbif.org/v1/species/search"
    params = {
        "q": scientific_name,
        "limit": 1  # Limit to top result
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error if request failed
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def savetojson(data,filename="output.json"):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

# Example usage:
if __name__ == "__main__":
    species_name = "Acanthurus gahhm"  # Replace with any species name
    result = fetch_species_data(species_name)
    savetojson(result)
