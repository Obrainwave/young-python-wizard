from datetime import datetime
from models.entry import Entry
from storage.file_storage import FileStorage

class JournalService:
    def __init__(self, storage: FileStorage):
        self.storage = storage
        self.entries = []   # In-memory list of Entry objects
        self._load_entries()

    def _load_entries(self):
        """Load entries from storage into memory."""
        self.entries = self.storage.load_entries()
        # Assign new IDs if entries lack them (e.g., from corrupted data)
        max_id = max([e.id for e in self.entries if e.id is not None], default=0)
        for entry in self.entries:
            if entry.id is None:
                max_id += 1
                entry.id = max_id

    def _save_entries(self):
        """Persist the current in-memory list to storage."""
        self.storage.save_entries(self.entries)

    def create_entry(self, title, content, tags=None):
        """Create a new entry and return it."""
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        new_id = max([e.id for e in self.entries], default=0) + 1
        entry = Entry(
            entry_id=new_id,
            title=title.strip(),
            content=content.strip(),
            timestamp=datetime.now().isoformat(timespec='seconds'),
            tags=tags if tags else []
        )
        self.entries.append(entry)
        self._save_entries()
        return entry

    def get_all_entries(self):
        """Return all entries sorted by timestamp descending (newest first)."""
        return sorted(self.entries, key=lambda e: e.timestamp, reverse=True)

    def get_entry_by_id(self, entry_id):
        """Return an entry by its ID, or None if not found."""
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    def search_entries(self, term):
        """Search entries by title, content, or tags. Returns list of matching entries."""
        term_lower = term.lower()
        results = []
        for entry in self.entries:
            if (term_lower in entry.title.lower() or
                term_lower in entry.content.lower() or
                any(term_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
        return results

    def update_entry(self, entry_id, title=None, content=None, tags=None):
        """Update an existing entry. Only provided fields are modified."""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            raise ValueError("Entry not found.")
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty.")
            entry.title = title.strip()
        if content is not None:
            entry.content = content.strip()
        if tags is not None:
            entry.tags = tags
        entry.timestamp = datetime.now().isoformat(timespec='seconds')   # update timestamp
        self._save_entries()
        return entry

    def delete_entry(self, entry_id):
        """Delete an entry by ID. Returns True if successful, False if not found."""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            return False
        self.entries.remove(entry)
        self._save_entries()
        return True