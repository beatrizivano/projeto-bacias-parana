import csv
import requests
from config.settings import QUERIES, ACCESSION_GENE_CSV, GENE_QUERIES
import os
from dotenv import load_dotenv

load_dotenv()

queries = {}
for file_path in QUERIES.iterdir():
    if file_path.is_file():
        river = file_path.stem
        with file_path.open("r", encoding="utf-8") as file:
            query = file.read()

            for gene, geneQuery in GENE_QUERIES.items():
                queries.setdefault(river, {})[gene] = query + geneQuery

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

params = {
    "email": os.getenv("EMAIL"),
    "apikey": os.getenv("API_KEY"),
    "retmax": 1000000000,
    "db": "nucleotide",
    "retmode": "json",
    "idtype": "acc"
}

results = []
for river, genes in queries.items():
    for gene, query in genes.items():
        req = requests.post(url, data=params | { "term": query })
        res = req.json().get("esearchresult")
        ids = res.get("idlist", None)

        if ids is not None:
            for id in ids:
                results.append({
                    "accession": id,
                    "gene": gene,
                    "river": river
                })
fieldnames = results[0].keys()

with open(ACCESSION_GENE_CSV, 'w', newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames,  restval='')
    writer.writeheader()
    writer.writerows(results)
