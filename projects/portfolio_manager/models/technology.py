class Technology:
    def __init__(self, technology_id=None, name=""):
        self.id = technology_id
        self.name = name

    def __repr__(self):
        return f"Technology(id={self.id}, name='{self.name}')"