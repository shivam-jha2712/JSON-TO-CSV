# JSON to CSV Converter

This repository contains a Python utility to convert a nested JSON file into CSV format.

## Files

- `json_to_csv_converter.py` — converter script
- `source/` — place input JSON files here
- `result/` — generated CSV files are written here

## Usage (PowerShell)

Run these exact commands:

```powershell
Set-Location "c:\Practice Code\JSON TO CSV"
python .\json_to_csv_converter.py --source ".\source\sample.json" --result ".\result"
Get-Content ".\result\sample.csv"
```

If your source file name is different:

```powershell
python .\json_to_csv_converter.py --source ".\source\YOUR_FILE.json" --result ".\result" --output "final.csv"
Get-Content ".\result\final.csv"
```

If `python` is not recognized, use `py` instead of `python` in the same commands.

## Usage (Command Prompt / CMD)

Run these exact commands:

```cmd
1. cd /d "c:\Practice Code\JSON TO CSV"
2. python json_to_csv_converter.py --source "source\sample.json" --result "result"
3. type "result\result.csv" (Optional)
```

If your source file name is different:

```cmd
python json_to_csv_converter.py --source "source\YOUR_FILE.json" --result "result"
type "result\YOUR_FILE.csv"
```

If `python` is not recognized, use `py` instead of `python` in the same commands.

## Behavior

- Accepts a top-level JSON object/dictionary.
- Flattens nested objects with `__` as separator.
- Produces combined rows from top-level arrays/objects using row index alignment.
- Creates the result folder automatically if missing.