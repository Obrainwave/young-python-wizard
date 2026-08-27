class SearchHistory:
    def __init__(self, id=None, city="", temperature=None, windspeed=None, searched_at=""):
        self.id = id
        self.city = city
        self.temperature = temperature
        self.windspeed = windspeed
        self.searched_at = searched_at

    def __repr__(self):
        return (f"SearchHistory(id={self.id}, city='{self.city}', "
                f"temperature={self.temperature}, windspeed={self.windspeed}, "
                f"searched_at='{self.searched_at}')")