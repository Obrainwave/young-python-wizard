# Weather Application

A command-line application that fetches real-time weather data from the Open-Meteo API (no API key required). It allows users to check weather for any city, save favorite cities, and view search history. Built with Python, SQLite, and the `requests` library, this project demonstrates clean object-oriented architecture with separated models, services, and storage layers.

This project is part of the **Young Python Wizard** series and is designed to teach how to build maintainable, production-ready applications with API integration.

---

## Features

- 🌦️ Fetch current weather (temperature, wind speed, condition) for any city.
- 📍 Geocoding: converts city names to coordinates automatically.
- ⭐ Save favorite cities for quick access (stores coordinates).
- 🕒 Search history: every weather check is saved locally.
- 🧹 Clear search history.
- 💾 Persistent storage using SQLite.
- 🔒 No API key required – uses Open-Meteo free API.

---

## Project Structure

```
weather_app/
├── models/
│   ├── __init__.py
│   ├── weather.py
│   ├── favorite.py
│   └── search_history.py
├── services/
│   ├── __init__.py
│   └── weather_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── favorite_repository.py
│   └── search_history_repository.py
├── requirements.txt
└── main.py
```

- **`models/`** – Data classes (`WeatherData`, `FavoriteCity`, `SearchHistory`).
- **`services/`** – Business logic and API communication (`WeatherService`).
- **`storage/`** – Database connection, initialization, and repositories.
- **`requirements.txt`** – Dependencies (only `requests`).
- **`main.py`** – Command-line interface and menu loop.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `requests` library

### Installation

1. Clone or download this repository.
2. Navigate to the `weather_app` folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

The first run will create a database file named `weather.db`.

---

## Usage

When you run the program, you'll see a menu:

```
--- Weather Application ---
1. Check Weather for a City
2. Add City to Favorites
3. View Favorites
4. Remove Favorite
5. View Search History
6. Clear Search History
7. Exit
Choose:
```

### Check Weather for a City

Enter a city name. The app geocodes the city, fetches current weather, displays temperature, wind speed, and condition. The search is saved to history.

### Add City to Favorites

Saves a city with its coordinates for quick reference.

### View Favorites

Lists all saved favorite cities.

### Remove Favorite

Deletes a favorite by ID.

### View Search History

Shows recent searches (most recent first, up to 50).

### Clear Search History

Deletes all search history records.

---

## How It Works

### Database Initialization

`DatabaseInitializer` checks whether the required tables (`favorites`, `search_history`) exist. If any are missing, it creates both tables.

### API Integration

- **Geocoding API**: `https://geocoding-api.open-meteo.com/v1/search` – converts city name to latitude/longitude.
- **Forecast API**: `https://api.open-meteo.com/v1/forecast` – returns current weather using `current_weather=true`.

The `WeatherService` class encapsulates all API calls and error handling. It uses `requests.get` with timeouts and `raise_for_status()`.

### Search History

Each time the user checks weather for a city, a `SearchHistory` record is created with the city name, temperature, windspeed, and timestamp. This is stored in SQLite.

### Favorites

Favorite cities store their coordinates, so subsequent lookups (not implemented in UI but possible in service) could skip geocoding.

---

## Extending the Project

Here are some ideas to enhance the application:

- Add unit conversion (Celsius ↔ Fahrenheit).
- Fetch and display humidity, precipitation, and cloud cover.
- Add a GUI using Tkinter.
- Implement auto-refresh for favorite cities.
- Export search history to CSV.
- Add unit tests using `pytest` and mocking API calls.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy coding! 🌤️🐍