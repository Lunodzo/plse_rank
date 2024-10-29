import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Base URL to extract the district's result links
base_url = "https://matokeo.necta.go.tz/results/2024/pslexj6/2024/distr_2606.htm"

def fetch_school_results():
    # Fetch the main page content
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # List to store results
    school_results = []

    # Find all links on the main page
    for link in soup.find_all("a", href=True):
        school_name = link.text.strip()
        school_url = f"https://matokeo.necta.go.tz/results/2024/pslexj6/2024/{link['href']}"
        
        # Fetch each school's page content
        school_response = requests.get(school_url)
        school_response.raise_for_status()
        school_soup = BeautifulSoup(school_response.text, "html.parser")
        
        # Find "WASTANI WA SHULE" in the content
        content_text = school_soup.get_text()
        match = re.search(r"WASTANI WA SHULE\s*:\s*([\d.]+)", content_text)
        
        # If the "WASTANI WA SHULE" value is found, record it
        if match:
            wastani_wa_shule = match.group(1)
            school_results.append({"School Name": school_name, "Wastani wa Shule": wastani_wa_shule})
        else:
            school_results.append({"School Name": school_name, "Wastani wa Shule": "Not Found"})
    
    # Convert results to a DataFrame and save as CSV
    df = pd.DataFrame(school_results)
    df.to_csv("school_results.csv", index=False)
    print("Results saved to school_results.csv")

# Run the function
fetch_school_results()
