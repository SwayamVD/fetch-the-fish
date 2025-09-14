from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

BASE_URL = "https://www.marinespecies.org/rest"

def get_species_info(species_name):
    """Search for species and return AphiaID + details."""
    search_url = f"{BASE_URL}/AphiaRecordsByMatchNames?scientificnames[]={species_name}&marine_only=true"
    response = requests.get(search_url)
    
    if response.status_code == 200 and response.json():
        record = response.json()[0][0]
        aphia_id = record.get("AphiaID")
        
        # Fetch full details
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
    
    return {"error": f"No data found for '{species_name}'"}

@app.route("/", methods=["GET"])
def home():
    api_doc = {
        "message": "...WELCOME TO OUR API...",
        "endpoints": {
            "/species?name=<species_name>": "Fetch species details by scientific name",
        },
        "example_usage": {
            "by_name": "/species?name=Thunnus albacares",
        }
    }
    return jsonify(api_doc)

@app.route("/species", methods=["GET"])
def species_api():
    """API endpoint to fetch species info."""
    species_name = request.args.get("name")
    if not species_name:
        return jsonify({"error": "Please provide a species name using ?name= parameter"}), 400
    
    result = get_species_info(species_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
