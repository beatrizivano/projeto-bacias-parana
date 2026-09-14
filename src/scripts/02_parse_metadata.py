from config.settings import GENBANK_RECORDS, ACCESSION_GENE_CSV, PARSED_GB_RECS, EXPECTED_QUALIFIERS
from Bio import SeqIO
import csv

lookup = {}
with open(ACCESSION_GENE_CSV, "r") as acc_gene_list:
    reader = csv.DictReader(acc_gene_list)
    for row in reader:
        lookup[row["accession"]] = row["gene"]

results = []
with open(GENBANK_RECORDS, "r") as records:
    for record in SeqIO.parse(records, "gb"):
        
        id = record.id
        organism = record.annotations.get("organism", None)
        gene = lookup.get(id, None)
        references = record.annotations.get("references", None)
        
        qualifier_data = {}
        for feature in record.features:
            for qualifier in feature.qualifiers.keys():
                if qualifier in EXPECTED_QUALIFIERS:
                    data = feature.qualifiers.get(qualifier, None)
                    qualifier_data[qualifier] = data[0]

        results.append({
            'id': id, 
            'organism': organism,
            'gene': gene,
            'references': references
            } | 
            qualifier_data
            )
        
REC_KEYS = ["id", "organism", "gene", "references"]

with open(PARSED_GB_RECS, "w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=REC_KEYS + EXPECTED_QUALIFIERS,  restval='')
    writer.writeheader()
    writer.writerows(results)

'''
accession - id
nome utilizado no registro -organism
gene - source_gene accession_gene
base de origem;
localidade; - x
país; - x
coordenadas - lat_lon
referência bibliográfica - references 
voucher/specimen; - specimen_voucher
metadata disponível.
'''

'''
actual_qualifiers
['PCR_primers', 'altitude', 'anticodon', 'artificial_location', 'bio_material', 'breed', 'chromosome', 'clone', 'clone_lib', 'codon_recognized', 'codon_start', 'collected_by', 'collection_date', 'common', 'db_xref', 'dev_stage', 'direction', 'ecotype', 'environmental_sample', 'estimated_length', 'experiment', 'gap_type', 'gene', 'gene_synonym', 'genotype', 'geo_loc_name', 'haplotype', 'host', 'identified_by', 'isolate', 'isolation_source', 'lab_host', 'lat_lon', 'linkage_evidence', 'linkage_group', 'locus_tag', 'map', 'mol_type', 'ncRNA_class', 'note', 'organelle', 'organism', 'product', 'protein_id', 'pseudo', 'replace', 'rpt_family', 'rpt_type', 'rpt_unit_range', 'rpt_unit_seq', 'sex', 'specimen_voucher', 'standard_name', 'strain', 'sub_species', 'submitter_seqid', 'tissue_type', 'transcript_id', 'transl_except', 'transl_table', 'translation']

#record.annotations.keys() = ['molecule_type', 'topology', 'data_file_division', 'date', 'accessions', 'sequence_version', 'keywords', 'source', 'organism', 'taxonomy', 'references']
'''

