class Contact:
    def __init__(self, contact_id=None, name="", phone="", email="", address=""):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __repr__(self):
        return (f"Contact(id={self.id}, name='{self.name}', phone='{self.phone}', "
                f"email='{self.email}', address='{self.address}')")