from config.settings import PARSED_GB_RECS, VALID_NAMES, RECONCILED_TAXONOMY, REVISIT_RECS
import csv

lookup = {}
with open(VALID_NAMES, "r") as valid_names:
    reader = csv.DictReader(valid_names)
    for row in reader:
        key = row["alias_name"]
        val = row["valid_name"]
        lookup[key] = val

results = []
revisit = []
with open(PARSED_GB_RECS, "r") as gb_recs:
    reader = csv.DictReader(gb_recs)
    for row in reader:
        alias = row["organism"].lower().strip()
        valid_name = lookup.get(alias, None)

        if not valid_name:
            revisit.append(row)
        else:
            results.append(row | {"organism": alias, "valid_name": valid_name})

with open(RECONCILED_TAXONOMY, "w", newline="") as reconciled_recs, open(REVISIT_RECS, "w", newline="") as revisit_recs:
    fieldnames = ['id','organism','valid_name','gene','references','collection_date','isolate','db_xref','geo_loc_name','lat_lon','specimen_voucher']
   
    reconciled_writer = csv.DictWriter(reconciled_recs, fieldnames=fieldnames)
    reconciled_writer.writeheader()
    reconciled_writer.writerows(results)

    revisit_writer = csv.DictWriter(revisit_recs, fieldnames=fieldnames)
    revisit_writer.writeheader()
    revisit_writer.writerows(revisit)