import datetime
import threading
import requests

from app.config.config import (
    WEATHER_WIDGET_API_KEY,
    WEATHER_WIDGET_IMAGE_SUNNY,
    WEATHER_WIDGET_IMAGE_CLOUDY,
    WEATHER_WIDGET_IMAGE_RAINY
)

class WeatherClockController:
    def __init__(self, view, city="Wiehl"):
        self.view = view
        self.city = city
        self.view.set_controller(self)

    def start(self):
        self.update_clock()
        self.update_weather()

    def update_clock(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S - %d.%m.%Y")
        day_of_week = now.strftime("%A")
        self.view.update_clock(time_str, day_of_week, self.city)
        self.view.after(1000, self.update_clock)

    def update_weather(self):
        def fetch():
            temp, condition, icon = self.get_weather(self.city)
            bg_path = self.get_background_path(icon)
            self.view.update_weather(temp, condition, bg_path, icon)
            self.view.after(600000, self.update_weather)
        threading.Thread(target=fetch, daemon=True).start()

    def get_weather(self, city):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_WIDGET_API_KEY}&units=metric&lang=en"
            response = requests.get(url)
            data = response.json()

            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            icon_code = data['weather'][0]['icon']

            return f"{temp:.1f}°C", weather.capitalize(), icon_code
        except Exception as e:
            print(f"[Erro ao consultar clima]: {e}")
            return "--°C", "Erro", "01d"

    def get_background_path(self, icon):
        if icon in ["01d", "02d"]:
            return WEATHER_WIDGET_IMAGE_SUNNY
        elif icon in ["03d", "04d"]:
            return WEATHER_WIDGET_IMAGE_CLOUDY
        elif icon in ["09d", "10d", "11d", "13d", "50d"]:
            return WEATHER_WIDGET_IMAGE_RAINY
        return WEATHER_WIDGET_IMAGE_CLOUDY