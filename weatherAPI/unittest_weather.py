from weather import Weather
import unittest

class TestWeather(unittest.TestCase):
    def test_isRaining(self):
        weather = Weather()
        res1 = weather.get_weather()
        expected = res1 == 'Rain'
        res2 = weather.is_raining()
        self.assertEqual(expected, res2)

    def test_setPlaceName_true(self):
        weather = Weather()
        place_name = "Chuncheon, KR"
        res = weather.set_placename(place_name=place_name)
        self.assertEqual("OK, changed the place name to " + place_name + "!", res)

    def test_setPlaceName_false(self):
        weather = Weather()
        place_name = "efawegawgawgewgawe"
        res = weather.set_placename(place_name=place_name)
        self.assertEqual("The place name is not correct!", res)

    def test_setPlaceName_none(self):
        weather = Weather()
        res = weather.set_placename(place_name="")
        self.assertEqual("The place name is not correct!", res)

    def test_setLocation_true(self):
        weather = Weather()
        lon, lat = 133, 43
        res = weather.set_location(lon=lon, lat=lat)
        self.assertEqual("OK, changed the location to longitude = " + str(lon) + ", latitude = " + str(lat) + "!", res)

    def test_setLocation_false(self):
        weather = Weather()
        lon, lat = 133, -96
        res = weather.set_location(lon=lon, lat=lat)
        self.assertEqual("Please set longitude, latitude! (-180 < longitude < 180, -90 < latitude < 90)", res)

    def test_changeMode_true_PlaceName(self):
        weather = Weather()
        res = weather.change_mode(mode_name="PlaceName")
        self.assertEqual("Change to PlaceName Mode", res)

    def test_changeMode_true_Loaction(self):
        weather = Weather()
        res = weather.change_mode(mode_name="Location")
        self.assertEqual("Change to Location Mode", res)

    def test_changeMode_false(self):
        weather = Weather()
        res = weather.change_mode(mode_name="aaaa")
        self.assertEqual("Please set PlaceName or Location", res)

if __name__ == "__main__":
    unittest.main()