## Input Files

- Minimal TSV
- VCF
- Phenopacket
- ClinVar Excel Templates

## Operations

- convert FROM/TO=        - Sub set of data interpreted
    - clinvar-xlsx

- batches
    - add variants to batch
    - modify batch as YAML via $EDITOR
    - delete batch
    - stores meta data, allows for later easier modification

- submission via API
    - submission
    - update
    - deletion

## Storage Locations

- config, default ~/.config/clinvar-this
- workspace, default ~/.local/share/clinvar-this/DEFAULT
