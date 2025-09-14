import requests
import pandas as pd
import os

BASE_URL = "https://www.marinespecies.org/rest"
OUTPUT_FILE = "marine_species_full.csv"

def get_species_info(species_name):
    """Search for species and return AphiaID + details."""
    # First: search by species name
    search_url = f"{BASE_URL}/AphiaRecordsByMatchNames?scientificnames[]={species_name}&marine_only=true"
    response = requests.get(search_url)
    
    if response.status_code == 200 and response.json():
        record = response.json()[0][0]
        aphia_id = record.get("AphiaID")
        
        # Now: fetch full details by AphiaID
        detail_url = f"{BASE_URL}/AphiaRecordByAphiaID/{aphia_id}"
        detail_response = requests.get(detail_url)
        
        if detail_response.status_code == 200:
            data = detail_response.json()
            species_data = {
                "ScientificName": data.get("scientificname", ""),
                "AphiaID": data.get("AphiaID", ""),
                "Status": data.get("status", ""),
                "AcceptedName": data.get("valid_name", ""),
                "Rank": data.get("rank", ""),
                "Kingdom": data.get("kingdom", ""),
                "Phylum": data.get("phylum", ""),
                "Class": data.get("class", ""),
                "Order": data.get("order", ""),
                "Family": data.get("family", ""),
                "Genus": data.get("genus", ""),
                "Environment": data.get("environment", ""),
                "OriginalName": data.get("originalname", ""),
                "Citation": data.get("citation", ""),
                "LSID": data.get("lsid", ""),
                "URL": f"https://www.marinespecies.org/aphia.php?p=taxdetails&id={aphia_id}"
            }
            return species_data
    
    print(f"❌ No data found for {species_name}")
    return None

def save_species_info(species_data):
    """Save species info to CSV, update if exists."""
    if species_data is None:
        return
    
    new_df = pd.DataFrame([species_data])
    
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)
        # Drop old entry if exists
        df = df[df["ScientificName"] != species_data["ScientificName"]]
        combined = pd.concat([df, new_df], ignore_index=True)
    else:
        combined = new_df
    
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved/updated {species_data['ScientificName']} in {OUTPUT_FILE}")

if __name__ == "__main__":
    species_list = [
        "Hemigymnus melapterus",
    ]
    
    for sp in species_list:
        info = get_species_info(sp)
        print(info)
        save_species_info(info)
