log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

run_stage() {
    local name="$1"
    local script="$2"
    log "$name"
    python "$script"
}

run_stage "stage 00: consolidating accessions" "scripts/00_consolidate_accessions.py"
run_stage "stage 01: fetching GB entries" "scripts/01_fetch_entries.py"
run_stage "stage 02: parsing metadata" "scripts/02_parse_metadata.py"
run_stage "stage 03: reconciling taxonomy" "scripts/03_reconcile_taxonomy.py"
run_stage "stage 04: classifying reliability and relevance" "scripts/04_classify_reliability_relevance.py"
run_stage "stage 05: summarizing" "scripts/05_summarize.py"