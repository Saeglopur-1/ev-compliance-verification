# src/data_collection.py
import requests
from pathlib import Path

def download_regulations():
    eu_regs = {
        "co2": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R0631",
        "battery": "https://eur-lex.europa.eu/eli/reg/2023/1542/oj"
    }
    
    for name, url in eu_regs.items():
        response = requests.get(url)
        Path(f"data/raw/{name}_regulation.pdf").write_bytes(response.content)