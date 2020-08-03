from weather import Weather

weather = Weather()

print(weather.place, weather.lon, weather.lat, weather.mode)
print(weather.get_weather())
print("----------")
print(weather.is_raining())
print("----------")
print(weather.set_plase(place_name="Chuncheon, KR"))
print(weather.set_location(lon=141, lat=43))
print("----------")
print(weather.get_weather())
weather.change_mode(mode_name="Location")
print(weather.get_weather())
print(weather.place, weather.lon, weather.lat, weather.mode)