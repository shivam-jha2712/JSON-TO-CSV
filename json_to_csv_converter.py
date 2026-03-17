import os
import csv
import json
import argparse
from typing import Any, Dict, List

def flatten_record(record: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Flatten one JSON object.
    Example:
      {"a": {"b": 1}, "c": 2} -> {"a__b": 1, "c": 2}
    """
    out = {}
    for k, v in record.items():
        col = f"{prefix}__{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten_record(v, col))
        else:
            out[col] = v
    return out

def build_rows_from_top_level(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build CSV rows from top-level JSON keys.
    - If top-level value is a list of objects => flattened with <topkey>__<field>
    - If top-level value is a list of primitives => <topkey>
    - If top-level value is object => treated as single item list
    - If top-level value is primitive => treated as single item list

    Rows are created using max length across all top-level keys.
    For row i, each section uses i-th element if available, else blanks.
    """
    prepared: Dict[str, List[Dict[str, Any]]] = {}

    for top_key, value in json_data.items():
        rows_for_key: List[Dict[str, Any]] = []

        if isinstance(value, list):
            if len(value) == 0:
                rows_for_key = []
            else:
                for item in value:
                    if isinstance(item, dict):
                        flat = flatten_record(item, top_key)
                        rows_for_key.append(flat)
                    else:
                        rows_for_key.append({top_key: item})

        elif isinstance(value, dict):
            rows_for_key = [flatten_record(value, top_key)]
        else:
            rows_for_key = [{top_key: value}]

        prepared[top_key] = rows_for_key

    max_len = max((len(v) for v in prepared.values()), default=0)

    all_rows: List[Dict[str, Any]] = []
    for i in range(max_len):
        row: Dict[str, Any] = {}
        for top_key, rows in prepared.items():
            if i < len(rows):
                row.update(rows[i])
        all_rows.append(row)

    return all_rows

def write_csv(rows: List[Dict[str, Any]], output_csv_path: str) -> None:
    # Collect all columns in order of first appearance
    fieldnames: List[str] = []
    seen = set()

    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def convert_json_to_csv(source_json_path: str, result_folder_path: str, output_filename: str = None) -> str:
    if not os.path.isfile(source_json_path):
        raise FileNotFoundError(f"Source JSON file not found: {source_json_path}")

    with open(source_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object/dictionary (as in your sample).")

    rows = build_rows_from_top_level(data)

    if output_filename is None:
        base = os.path.splitext(os.path.basename(source_json_path))[0]
        output_filename = f"{base}.csv"

    output_csv_path = os.path.join(result_folder_path, output_filename)
    write_csv(rows, output_csv_path)
    return output_csv_path

def main():
    parser = argparse.ArgumentParser(description="Convert nested JSON to CSV.")
    parser.add_argument("--source", required=True, help="Path to source JSON file")
    parser.add_argument("--result", required=True, help="Path to result folder")
    parser.add_argument("--output", required=False, help="Optional output CSV filename (e.g., result2.csv)")
    args = parser.parse_args()

    output_path = convert_json_to_csv(args.source, args.result, args.output)
    print(f"✅ CSV created: {output_path}")

if __name__ == "__main__":
    main()
