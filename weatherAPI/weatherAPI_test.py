import requests
import json
import os

city_name = "efawegawgawgewgawe"#"Chuncheon, KR"
API_KEY = os.environ['weatherapi_key']
lon, lat = 141, 43 #longitude, latitude 経度 経度
part = "minutely"
units = "metric"

# Current Weather Data
# use city name
api = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={city}&APPID={key}"
url = api.format(units = units, city = city_name, key = API_KEY)
# use longitude, latitude
#api = "http://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&APPID={key}"
#url = api.format(units = units, city = city_name, lon = lon, lat = lat, key = API_KEY)

# one call
#api = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&units={units}&appid={key}"
#url = api.format(lat = lat, lon = lon, part = part, units = units, key = API_KEY)

print(url)
res = requests.get(url)
print(res.status_code)
data = res.json()
jsonText = json.dumps(data, indent=4)
print(jsonText)

print(data['weather'][0]['main'])