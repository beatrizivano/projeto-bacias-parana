from pathlib import Path

#folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA = PROJECT_ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
FINAL = DATA / "final"
QUERIES = RAW / "queries"

#files
VALID_NAMES = RAW / "valid_names.csv"
ACCESSIONS = INTERIM / "accessions.json"
ENTRIES = INTERIM / "entries.gb"
RECORDS = INTERIM / "records.json"
RECONCILED_TAXONOMY = INTERIM / "reconciled_taxonomy.csv"
REVISIT_RECS = INTERIM / "revisit_recs.csv"
ADDRESSES = INTERIM / "addresses.csv"
RELIABILITY_CLASS = FINAL / "reliability_class.csv"
SUMMARY = FINAL / "summary.xlsx"