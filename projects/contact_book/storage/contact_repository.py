from models.contact import Contact

class ContactRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, contact):
        self.db.execute(
            "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
            (contact.name, contact.phone, contact.email, contact.address)
        )
        self.db.commit()
        contact.id = self.db.last_row_id()
        return contact

    def get_by_id(self, contact_id):
        self.db.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = self.db.fetchone()
        if row:
            return self._row_to_contact(row)
        return None

    def get_all(self):
        self.db.execute("SELECT * FROM contacts ORDER BY name")
        rows = self.db.fetchall()
        return [self._row_to_contact(row) for row in rows]

    def search(self, term):
        """Search contacts by name, phone, or email (case-insensitive)."""
        self.db.execute(
            "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? ORDER BY name",
            (f"%{term}%", f"%{term}%", f"%{term}%")
        )
        rows = self.db.fetchall()
        return [self._row_to_contact(row) for row in rows]

    def update(self, contact):
        self.db.execute(
            "UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
            (contact.name, contact.phone, contact.email, contact.address, contact.id)
        )
        self.db.commit()

    def delete(self, contact_id):
        self.db.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        self.db.commit()

    def _row_to_contact(self, row):
        return Contact(
            contact_id=row["id"],
            name=row["name"],
            phone=row["phone"],
            email=row["email"],
            address=row["address"]
        )