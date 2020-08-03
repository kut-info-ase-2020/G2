import requests
import json
import os

class Weather:
    def __init__(self):
        self.mode = 0
        self.place = "Kochi,jp"
        self.lon, self.lat = 133, 33 #longitude, latitude 経度 経度
        self.part = "minutely"
        self.units = "metric"
        self.API_KEY = os.environ['weatherapi_key']

    def get_weather(self):
        if self.mode == 0:
            api = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&APPID={key}"
            url = api.format(units = self.units, city = self.place, key = self.API_KEY)
        else:
            api = "http://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&APPID={key}"
            url = api.format(units = self.units, lon = self.lon, lat = self.lat, key = self.API_KEY)

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            weather = data['weather'][0]['main']
            return data['weather'][0]['main']
        
        return "Error"

    def is_raining(self):
        weather = self.get_weather()
        if weather == "Rain":
            return True
        return False

    def set_plase(self, place_name):
        api = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&APPID={key}"
        url = api.format(units = self.units, city = place_name, key = self.API_KEY)

        res = requests.get(url)
        if res.status_code == 200:
            self.place = place_name
            return "OK, changed it!"
        else:
            return "The name is not correct!"

    def set_location(self, lon, lat):
        api = "http://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&APPID={key}"
        url = api.format(units = self.units, lon = lon, lat = lat, key = self.API_KEY)

        res = requests.get(url)
        if res.status_code == 200:
            self.lon = lon
            self.lat = lat
            return "OK, changed it!"
        else:
            return "The place name is not correct!"

    def change_mode(self, mode_name):
        if mode_name == "PlaceName":
            self.mode = 0
        elif mode_name == "Location":
            self.mode = 1
        else:
            return "Please set PlaceName or Location"
    
