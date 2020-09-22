import requests
import json
import os

class Weather:
    def __init__(self):
        self.setting_list_path = "weather.json"
        if os.path.isfile(self.setting_list_path):
            with open(self.setting_list_path, 'r') as json_file:
                self.setting_list = json.load(json_file)
                self.mode = self.setting_list['mode']
                self.place_name = self.setting_list['place_name']
                self.lon = self.setting_list['location']['longitude']
                self.lat = self.setting_list['location']['latitude']
                self.part = self.setting_list['part']
                self.units = self.setting_list['units']
                self.API_KEY = self.setting_list['API_KEY']

        else:
            self.mode = 0
            self.place_name = "Kochi,jp"
            self.lon, self.lat = 133, 33 #longitude, latitude 経度 経度
            self.part = "minutely"
            self.units = "metric"
            self.API_KEY = os.environ['weatherapi_key']
            self.setting_list = {
                "mode": self.mode,
                "place_name": self.place_name,
                "location": {"longitude": self.lon, "latitude": self.lat},
                "part": self.part,
                "units": self.units,
                "API_KEY": self.API_KEY,
            }
            with open(self.setting_list_path), 'w') as outfile:
                json.dump(self.setting_list, outfile)

    def get_weather(self):
        if self.mode == 0:
            api = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&APPID={key}"
            url = api.format(units = self.units, city = self.place_name, key = self.API_KEY)
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
        else:
            return False

    def set_placename(self, place_name):
        api = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&APPID={key}"
        url = api.format(units = self.units, city = place_name, key = self.API_KEY)

        res = requests.get(url)
        if res.status_code == 200:
            self.place_name = place_name
            with open(self.setting_list_path, "w") as json_file:
                self.setting_list['place_name'] = self.place_name
                json.dump(self.setting_list, json_file)
            return "OK, changed the place name to " + self.place_name + "!"
        else:
            return "The place name is not correct!"

    def set_location(self, lon, lat):
        api = "http://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&APPID={key}"
        url = api.format(units = self.units, lon = lon, lat = lat, key = self.API_KEY)

        res = requests.get(url)

        if lon < -180 or 180 < lon or lat < -90 or 90 < lat:
            return "Please set longitude, latitude! (-180 < longitude < 180, -90 < latitude < 90)"
        if res.status_code == 200:
            self.lon = lon
            self.lat = lat
            with open(self.setting_list_path, "w") as json_file:
                self.setting_list['location'] = {"longitude": self.lon, "latitude": self.lat}
                json.dump(self.setting_list, json_file)

            return "OK, changed the location to longitude = " + str(self.lon) + ", latitude = " + str(self.lat) + "!"
        else:
            return "The location is not correct!"

    def change_mode(self, mode_name):
        if mode_name == "PlaceName":
            self.mode = 0
            with open(self.setting_list_path, "w") as json_file:
                self.setting_list['mode'] = self.mode
                json.dump(self.setting_list, json_file)
            return "Change to PlaceName Mode"
        elif mode_name == "Location":
            self.mode = 1
            with open(self.setting_list_path, "w") as json_file:
                self.setting_list['mode'] = self.mode
                json.dump(self.setting_list, json_file)
            return "Change to Location Mode"
        else:
            return "Please set PlaceName or Location"

    def get_placenamme(self):
        return self.place_name
    
    def get_location(self):
        return {"longitude": self.lon, "latitude": self.lat}

    def get_mode(self):
        return self.mode

    def load_setting(self):
        with open(self.setting_list_path, "r") as json_file:
            self.setting_list = json.load(json_file)
            self.mode = self.setting_list['mode']
            self.place_name = self.setting_list['place_name']
            self.lon = self.setting_list['location']['longitude']
            self.lat = self.setting_list['location']['latitude']
            self.part = self.setting_list['part']
            self.units = self.setting_list['units']
            self.API_KEY = self.setting_list['API_KEY']