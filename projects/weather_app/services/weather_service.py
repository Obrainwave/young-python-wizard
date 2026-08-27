import requests
from datetime import datetime
from models.weather import WeatherData
from models.favorite import FavoriteCity
from models.search_history import SearchHistory
from storage.favorite_repository import FavoriteRepository
from storage.search_history_repository import SearchHistoryRepository

class WeatherService:
    def __init__(self, db):
        self.favorite_repo = FavoriteRepository(db)
        self.history_repo = SearchHistoryRepository(db)
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates(self, city):
        """Convert city name to (lat, lon, display_name) using geocoding API."""
        params = {"name": city, "count": 1, "language": "en", "format": "json"}
        response = requests.get(self.geocoding_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "results" not in data or not data["results"]:
            raise ValueError(f"City '{city}' not found.")
        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"]

    def get_weather(self, latitude, longitude):
        """Fetch current weather for coordinates and return WeatherData."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"
        }
        response = requests.get(self.forecast_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get("current_weather", {})
        return WeatherData(
            temperature=current.get("temperature"),
            windspeed=current.get("windspeed"),
            weathercode=current.get("weathercode"),
            time=current.get("time")
        )

    def fetch_weather_for_city(self, city):
        """Get coordinates and fetch weather. Returns (display_name, WeatherData)."""
        lat, lon, display_name = self.get_coordinates(city)
        weather = self.get_weather(lat, lon)
        # Save to search history
        history_entry = SearchHistory(
            city=display_name,
            temperature=weather.temperature,
            windspeed=weather.windspeed,
            searched_at=datetime.now().isoformat(timespec='seconds')
        )
        self.history_repo.insert(history_entry)
        return display_name, weather

    # Favorites operations
    def add_favorite(self, city):
        lat, lon, display_name = self.get_coordinates(city)
        existing = self.favorite_repo.get_by_city(display_name)
        if existing:
            raise ValueError(f"'{display_name}' is already in favorites.")
        favorite = FavoriteCity(
            city=display_name,
            latitude=lat,
            longitude=lon,
            added_at=datetime.now().isoformat(timespec='seconds')
        )
        return self.favorite_repo.insert(favorite)

    def get_favorites(self):
        return self.favorite_repo.get_all()

    def remove_favorite(self, favorite_id):
        self.favorite_repo.delete(favorite_id)

    # Search history operations
    def get_search_history(self):
        return self.history_repo.get_all()

    def clear_search_history(self):
        self.history_repo.delete_all()

    def weather_description(self, weathercode):
        """Convert WMO weather code to a simple description."""
        if weathercode is None:
            return "Unknown"
        if weathercode == 0:
            return "Clear sky"
        elif 1 <= weathercode <= 3:
            return "Partly cloudy"
        elif weathercode == 45 or weathercode == 48:
            return "Foggy"
        elif 51 <= weathercode <= 57:
            return "Drizzle"
        elif 61 <= weathercode <= 65:
            return "Rain"
        elif 71 <= weathercode <= 77:
            return "Snow"
        elif 80 <= weathercode <= 82:
            return "Rain showers"
        elif weathercode >= 95:
            return "Thunderstorm"
        else:
            return "Other"