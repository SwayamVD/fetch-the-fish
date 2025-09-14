import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL for POST request
url = "https://www.fishbase.se/ComNames/CommonNameSearchList.php"

# POST data payload
payload = {
    "crit1_fieldname": "COMNAMES.ComName",
    "lang": "English",
    "resultPage": "1",
    "crit1_fieldtype": "CHAR",
    "language": "All",
    "crit1_operator": "EQUAL",
    "CommonName": "surmai"
}

# Send POST request
response = requests.post(url, data=payload)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the table by id
table = soup.find("table", {"id": "table_filter"})
if not table:
    print("No table found")
    exit()

# Extract headers
headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

# Extract rows
rows = []
for tr in table.find("tbody").find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    rows.append(cols)

# Convert to DataFrame
df = pd.DataFrame(rows, columns=headers)

# Display and save
print(df)
df.to_csv("fishbase_comnames_surmai.csv", index=False)
