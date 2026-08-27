class WeatherData:
    def __init__(self, temperature=None, windspeed=None, weathercode=None, time=None):
        self.temperature = temperature
        self.windspeed = windspeed
        self.weathercode = weathercode
        self.time = time

    def __repr__(self):
        return (f"WeatherData(temperature={self.temperature}, windspeed={self.windspeed}, "
                f"weathercode={self.weathercode}, time='{self.time}')")