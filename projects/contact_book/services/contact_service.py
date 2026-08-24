from models.contact import Contact
from storage.contact_repository import ContactRepository

class ContactService:
    def __init__(self, db):
        self.repo = ContactRepository(db)

    def add_contact(self, name, phone="", email="", address=""):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        contact = Contact(name=name.strip(), phone=phone.strip(), email=email.strip(), address=address.strip())
        return self.repo.insert(contact)

    def get_all_contacts(self):
        return self.repo.get_all()

    def get_contact(self, contact_id):
        return self.repo.get_by_id(contact_id)

    def search_contacts(self, term):
        if not term.strip():
            return []
        return self.repo.search(term.strip())

    def update_contact(self, contact_id, name, phone="", email="", address=""):
        contact = self.repo.get_by_id(contact_id)
        if not contact:
            raise ValueError("Contact not found.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        contact.name = name.strip()
        contact.phone = phone.strip()
        contact.email = email.strip()
        contact.address = address.strip()
        self.repo.update(contact)
        return contact

    def delete_contact(self, contact_id):
        contact = self.repo.get_by_id(contact_id)
        if not contact:
            raise ValueError("Contact not found.")
        self.repo.delete(contact_id)