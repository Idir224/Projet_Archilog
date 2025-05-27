import csv
import io
import uuid
from datetime import datetime
import archilog.models as models

def export_to_csv() -> io.StringIO:
    entries = models.get_all_entries()
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["id", "name", "amount", "category", "date"])  # Header
    
    for entry in entries:
        writer.writerow([
            str(entry.id),  # UUID en string
            entry.name,
            entry.amount,
            entry.category or "",
            entry.date.isoformat()
        ])
    
    output.seek(0)
    return output

def import_from_csv(file) -> None:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            id = uuid.UUID(row["id"])  # Ignoré car non utilisé dans la création
            name = row["name"]
            amount = float(row["amount"])
            category = row.get("category") or None
            models.create_entry(name, amount, category)
        except Exception as e:
            print(f"Erreur lors de l'import d'une ligne : {e}")
