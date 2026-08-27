class FavoriteCity:
    def __init__(self, id=None, city="", latitude=0.0, longitude=0.0, added_at=""):
        self.id = id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.added_at = added_at

    def __repr__(self):
        return (f"FavoriteCity(id={self.id}, city='{self.city}', "
                f"latitude={self.latitude}, longitude={self.longitude}, added_at='{self.added_at}')")