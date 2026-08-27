import requests
from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.weather_service import WeatherService

def main():
    db = Database("weather.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = WeatherService(db)

    while True:
        print("\n--- Weather Application ---")
        print("1. Check Weather for a City")
        print("2. Add City to Favorites")
        print("3. View Favorites")
        print("4. Remove Favorite")
        print("5. View Search History")
        print("6. Clear Search History")
        print("7. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                city = input("Enter city name: ")
                display_name, weather = service.fetch_weather_for_city(city)
                print(f"\nWeather in {display_name}:")
                print(f"Temperature: {weather.temperature}°C")
                print(f"Wind speed: {weather.windspeed} km/h")
                print(f"Condition: {service.weather_description(weather.weathercode)}")
            elif choice == "2":
                city = input("Enter city name to save: ")
                fav = service.add_favorite(city)
                print(f"Added {fav.city} to favorites.")
            elif choice == "3":
                favorites = service.get_favorites()
                if not favorites:
                    print("No favorites saved.")
                else:
                    print("\nFavorites:")
                    for f in favorites:
                        print(f"ID: {f.id} | City: {f.city} | Lat: {f.latitude} | Lon: {f.longitude}")
            elif choice == "4":
                fav_id = int(input("Enter favorite ID to remove: "))
                service.remove_favorite(fav_id)
                print("Favorite removed.")
            elif choice == "5":
                history = service.get_search_history()
                if not history:
                    print("No search history.")
                else:
                    print("\nSearch History (most recent first):")
                    for h in history:
                        print(f"{h.searched_at} | {h.city} | Temp: {h.temperature}°C | Wind: {h.windspeed} km/h")
            elif choice == "6":
                service.clear_search_history()
                print("Search history cleared.")
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    db.close()

if __name__ == "__main__":
    main()