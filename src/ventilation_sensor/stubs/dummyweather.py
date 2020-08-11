from sys import stderr
class Weatherinfo:
    def get_today(self):
        print("dummy weather: returning " + self.weather_str, file=stderr)
        return self.weather_str
    def set_weather(self, weather):
        self.weather_str = weather
