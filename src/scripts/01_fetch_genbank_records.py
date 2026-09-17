from Bio import Entrez
from config.settings import ACCESSION_GENE_CSV, GENBANK_RECORDS
import csv
import http
import os
from dotenv import load_dotenv

load_dotenv()

Entrez.email = os.getenv("EMAIL")
Entrez.api = os.getenv("API_KEY")
accessions = []
chunk_size = 200

with open(ACCESSION_GENE_CSV, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        accessions.append(row['accession'])

with open(GENBANK_RECORDS, 'w') as outfile:
    for i in range(0, len(accessions), chunk_size):
        chunk = accessions[i : i + chunk_size]
        ids = ",".join(chunk)
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                handle = Entrez.efetch(db="nucleotide", id=ids, rettype="gb", retmode="text")
                content = handle.read()
                outfile.write(content)
            except http.client.IncompleteRead:
                attempts += 1
            finally:
                success = True