import json
import requests
from bs4 import BeautifulSoup, ResultSet, Tag

url = "https://learn.microsoft.com/en-us/connectors/connector-reference/"
response = requests.get(url)
if response.status_code != 200:
    print("Status code != 200")
    exit(1)
html = response.text
parsed_html = BeautifulSoup(html, features="html.parser")
cells: ResultSet[Tag] = parsed_html.find_all("td", attrs={"width": "25%"})

connectors = []

features = ["Logic Apps", "Power Automate", "Power Apps", "Preview", "Premium"]

for cell in cells:
    connector = {}

    tag_img = cell.find("img", recursive=False, attrs={"data-linktype": "external"})
    if type(tag_img) is Tag:
        # title -> name
        # src -> icon
        connector["DisplayName"] = tag_img.attrs["title"]
        connector["Icon"] = tag_img.attrs["src"]

    tag_a = cell.find("a", recursive=False)
    if type(tag_a) is Tag:
        # href path -> internalname
        href = tag_a.attrs["href"]
        last_slash = href[:-1].rfind("/") + 1
        connector["Name"] = tag_a.attrs["href"][last_slash:-1]
    
    connector["SearchTerms"] = (
        connector["Name"].lower() + " " + connector["DisplayName"].lower()
    )
    for feature in features:
        tag_feature = cell.find("img", recursive=False, attrs={"alt": feature})
        connector[feature] = tag_feature != None
    connectors.append(connector)
# Save JSON
json_output = json.dumps({"data": connectors}, separators=(",", ":"))
file = open("docs/connectors.json", "w", encoding="utf8")
file.write(json_output)
file.close()
