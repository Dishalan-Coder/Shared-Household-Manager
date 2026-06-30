"""CSV-only handler for bill uploads and downloads."""
import csv
import io
from fastapi import UploadFile, File, HTTPException

ALLOWED_EXT = ".csv"

def _validate_csv(filename: str):
    if not filename.lower().endswith(ALLOWED_EXT):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed for bill upload/download."
        )

async def parse_expenses_csv(file: UploadFile) -> list:
    _validate_csv(file.filename)
    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    required = {"description", "amount", "payer"}
    if not required.issubset({h.strip() for h in (reader.fieldnames or [])}):
        raise HTTPException(
            status_code=400,
            detail="CSV must include columns: description, amount, payer (+ optional date, split_between)"
        )
    rows = []
    for row in reader:
        rows.append({k.strip(): (v or "").strip() for k, v in row.items()})
    return rows

def generate_expenses_csv(expenses: list) -> str:
    """Convert expense list to CSV text."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["description", "amount", "payer", "date", "split_between"])
    for e in expenses:
        writer.writerow([
            e.get("description", ""),
            e.get("amount", 0),
            e.get("payer_name", ""),
            e.get("date", "")[:10] if e.get("date") else "",
            ", ".join(e.get("split_between_names", []))
        ])
    return output.getvalue()