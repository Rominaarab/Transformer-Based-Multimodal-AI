"""Verify the expression-to-GEO join without treating PFS as response."""
import argparse
import csv
import gzip
import json
import re


def sample_id(value):
    value = re.sub(r"\s+", "", value).upper()
    if not re.fullmatch(r"NSCLC\d+", value):
        raise ValueError(f"Unexpected NSCLC sample ID: {value}")
    return value


def audit(expression_path, metadata_path):
    with gzip.open(expression_path, "rt", encoding="utf-8-sig") as stream:
        header = next(csv.reader(stream, delimiter="\t"))
    if header[0] != "gene_id":
        raise ValueError("Expected the original GEO expression matrix with a gene_id column.")
    expression = list(map(sample_id, header[1:]))

    with gzip.open(metadata_path, "rt", encoding="utf-8-sig") as stream:
        rows = list(csv.reader(stream, delimiter="\t"))
    titles, accessions = (
        next(row[1:] for row in rows if row and row[0] == key)
        for key in ("!Sample_title", "!Sample_geo_accession")
    )
    metadata = list(map(sample_id, titles))
    mapping = dict(zip(metadata, accessions, strict=True))
    if len(mapping) != len(metadata) or len(set(accessions)) != len(accessions):
        raise ValueError("Duplicate GEO sample identifiers.")
    if len(set(expression)) != len(expression) or set(expression) != set(mapping):
        raise ValueError("Expression and GEO metadata do not match one to one.")
    characteristics = sorted({
        field.partition(":")[0].strip()
        for row in rows if row and row[0] == "!Sample_characteristics_ch1"
        for field in row[1:] if ":" in field
    })
    return {
        "matched_samples": len(expression),
        "expression_order_matches_metadata": expression == metadata,
        "characteristic_fields": characteristics,
        "expression_order_accessions": [mapping[sample] for sample in expression],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expression")
    parser.add_argument("metadata")
    args = parser.parse_args()
    print(json.dumps(audit(args.expression, args.metadata), indent=2))
