from dotenv import load_dotenv
from Bio import Entrez
from config.settings import ACCESSIONS, ENTRIES
import json
import http
import os

load_dotenv()

Entrez.email = os.getenv("EMAIL")
Entrez.api = os.getenv("API_KEY")
chunk_size = 200

with open(ACCESSIONS) as f:
    data = json.load(f)
    accessions = list(data.keys())

with open(ENTRIES, 'w') as f:
    for i in range(0, len(accessions), chunk_size):
        chunk = accessions[i : i + chunk_size]
        ids = ",".join(chunk)
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                handle = Entrez.efetch(db="nucleotide", id=ids, rettype="gb", retmode="text")
                content = handle.read()
                f.write(content)
            except http.client.IncompleteRead:
                attempts += 1
            finally:
                success = True