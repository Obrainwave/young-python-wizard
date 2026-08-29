import json
from pathlib import Path

from models.entry import Entry

class FileStorage:
    def __init__(self, filename="journal.json"):
        self.filename = Path(filename)

    def load_entries(self):
        """Load entries from the JSON file. Returns a list of Entry objects."""
        if not self.filename.exists():
            return []
        with self.filename.open("r") as f:
            data = json.load(f)
        return [Entry.from_dict(item) for item in data]

    def save_entries(self, entries):
        """Save a list of Entry objects to the JSON file."""
        data = [entry.to_dict() for entry in entries]
        with self.filename.open("w") as f:
            json.dump(data, f, indent=2)

    def ensure_file_exists(self):
        """Create the file if it does not exist."""
        if not self.filename.exists():
            self.filename.write_text("[]")