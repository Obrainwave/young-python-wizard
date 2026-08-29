class Entry:
    def __init__(self, entry_id=None, title="", content="", timestamp="", tags=None):
        self.id = entry_id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.tags = tags if tags is not None else []

    def to_dict(self):
        """Convert entry to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Entry object from a dictionary."""
        return cls(
            entry_id=data.get("id"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", ""),
            tags=data.get("tags", [])
        )

    def __repr__(self):
        return f"Entry(id={self.id}, title='{self.title}', timestamp='{self.timestamp}')"