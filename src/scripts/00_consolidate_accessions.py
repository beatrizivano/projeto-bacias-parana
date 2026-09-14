import csv
from Bio import SeqIO
from config.settings import GENE_FILE_MAP, FASTA_FOLDER, ACCESSION_GENE_CSV

results = []
for gene, file_list in GENE_FILE_MAP.items():
    for filename in file_list:
        for seq_rec in SeqIO.parse(FASTA_FOLDER / filename, "fasta"):
            results.append({"accession": seq_rec.id, "source_gene": gene})

with open(ACCESSION_GENE_CSV,'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["accession", "gene"])
    writer.writeheader()
    for row in results:
        writer.writerow({"accession": row["accession"], "gene": row["source_gene"]})