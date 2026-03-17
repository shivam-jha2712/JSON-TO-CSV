# JSON to CSV Converter

This repository contains a Python utility to convert a nested JSON file into CSV format.

## Files

- `json_to_csv_converter.py` — converter script
- `source/` — place input JSON files here
- `result/` — generated CSV files are written here

## Usage

```bash
python json_to_csv_converter.py --source "./source/result2.json" --result "./result" --output "result 2.csv"
```

## Behavior

- Accepts a top-level JSON object/dictionary.
- Flattens nested objects with `__` as separator.
- Produces combined rows from top-level arrays/objects using row index alignment.
- Creates the result folder automatically if missing.