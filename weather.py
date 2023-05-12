import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty


# pull data from file .env
load_dotenv()
api_key = os.getenv('API_KEY')    # crap API_KEY from file


# ############################## methods ##############################

# give me location information
def get_lan_lon(city_name, state_code, country_code, API_key):
    print("[method: get_lan_lon(city_name, state_code, country_code, API_key)] - call successful")
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()    #c consert response into valid json
    if not resp:
        print("[method: get_lan_lon] - ERROR: lat or lon missing. Set lat and lon default 'None'")
        return None, None
    else:
        print("[method: get_lan_lon] - Response successful")
        data = resp[0]
        lat , lon = data.get('lat'), data.get('lon')
        return lat, lon


# give me the location weather data
def get_current_weather(lat, lon, API_key):
    print("[method: get_current_weather(lat, lon, API_key)] - call successful")
    print(f"[method: get_current_wateher] lat: {lat}; lon: {lon}")
    resp = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()    # gave me back the weather data of the specific location

    try:
        rain = float(resp.get('rain').get('1h'))
    except Exception as e:
        print(f"Error getting rain data: {e}")
        rain = "None"

    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        decscription=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp')),
        humidity=float(resp.get('main').get('humidity')),
        wind=float(resp.get('wind').get('speed')),
        rain=rain
    )
    return data


# ############################## class ##############################

# The name of THIS class must be the same as the kv-file + 'App'
class OpenWeatherApp(App):
    print("[class: OpenWeatherApp(App)] - call successful")
    pass


class BoxLayoutExample(BoxLayout):
    print("[class: WeatherWidget(BoxLayout)] - call successful")
    my_image = StringProperty("10d")
    my_clouds = StringProperty("Clouds")
    my_description = StringProperty("Description")
    my_temperature = StringProperty("Temperature")
    my_humidity = StringProperty("Humidity")
    my_wind = StringProperty("Wind")
    my_rain = StringProperty("Rain")

    def on_button_click(self, widget, city, state, country):
        print("[method: on_button_click(self)] - button pressed")
        if city and state and country:
            print(f"{city}; {state}; {country}")
            lat, lon = get_lan_lon(city, state, country, api_key)
            if lat is None or lon is None:
                print("[method: on_button_click] - get_lan_lon() retrun error")
                widget.text = "ERROR: Location unknown"
            else:
                weather_data = get_current_weather(lat, lon, api_key)
                print(f"Main: {weather_data.main} | Description: {weather_data.decscription} | Temperature: {weather_data.temperature} | Icon: {weather_data.icon}")
                print("")
                self.my_image = weather_data.icon
                self.my_clouds = weather_data.main
                self.my_description = weather_data.decscription
                self.my_temperature = str(weather_data.temperature)
                self.my_humidity = str(weather_data.humidity)
                self.my_wind = str(weather_data.wind*3.6)
                self.my_rain = str(weather_data.rain)
                widget.text = "Search"
        else:
            print()
            widget.text = "ERROR: Missing inputs"   


# with '@dataclass' you dont need '__init__' and '__repr__' and '__eq__' method
@dataclass
class WeatherData:
    print("[class: WeatherDate] - call successful")
    main: str
    decscription: str
    icon: str
    temperature: int
    humidity: float
    wind: float
    rain: float


# ############################## __main__ ##############################

if __name__ == "__main__":
    print("[__main__] pass")
    OpenWeatherApp().run()
