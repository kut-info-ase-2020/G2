from sys import stderr
class Weather:
    weather_str = 'sunny'
    def get_today(self):
        print("dummy weather: returning " + self.weather_str, file=stderr)
        return self.weather_str
    def set_weather(self, weather):
        Weather.weather_str = weather
    def is_raining(self):
        if Weather.weather_str == 'rainy':
            return True
        return False
