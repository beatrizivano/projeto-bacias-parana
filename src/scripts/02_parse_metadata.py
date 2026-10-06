from config.settings import ENTRIES, ACCESSIONS, RECORDS
from config.params import EXPECTED_QUALIFIERS
from Bio import SeqIO
import csv
import json

#criar novo json, agora com info gb

with open(ACCESSIONS) as f:
    records = json.load(f)

with open(ENTRIES, "r") as f:
    for entry in SeqIO.parse(f, "gb"):
        id = entry.id
        organism = entry.annotations.get("organism", None)
        references = entry.annotations.get("references", None)
        
        metadata = {}
        for feature in entry.features:
            for qualifier in feature.qualifiers.keys():
                if qualifier in EXPECTED_QUALIFIERS:
                    data = feature.qualifiers.get(qualifier, None)
                    metadata[qualifier] = data[0]

        records[id]["organism"] = organism
        records[id]["references"] = references
        records[id]["metadata"] = metadata

with open(RECORDS, "w") as f:
    json.dump(records, f, indent=2)