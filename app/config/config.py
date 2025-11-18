import os

# Global Path
MAIN_IMGS_PATH = "app/assets/imgs"

# DB Path
DATABASE_PATH = os.path.join("app/data/database", "plataform.db")

# App Imagens Path
ICON_PATH = os.path.join(MAIN_IMGS_PATH, "logo1.png")

# Canvas Image Path
GRIDAI_PRO_IMAGE_PATH = os.path.join(MAIN_IMGS_PATH, "grid_32.png")
GRIDAI_HOME_IMAGE_PATH = os.path.join(MAIN_IMGS_PATH, "grid_14.png")

# Weather Widget
IMGS_WEATHER_WIDGET = "app/ui/widgets/weather/imgs"

WEATHER_WIDGET_IMAGE_SUNNY = os.path.join(IMGS_WEATHER_WIDGET, "sunny.jpg")
WEATHER_WIDGET_IMAGE_RAINY = os.path.join(IMGS_WEATHER_WIDGET, "rainy.jpg")
WEATHER_WIDGET_IMAGE_CLOUDY = os.path.join(IMGS_WEATHER_WIDGET, "cloudy.jpg")
WEATHER_WIDGET_IMAGE_PARTLY_CLOUDY = os.path.join(IMGS_WEATHER_WIDGET, "partly_cloudy.jpg")

WEATHER_WIDGET_API_KEY = "081c79c58728701d8ab9722f80157b16"

# App Icons main path
MAIN_ICONS_PATH = "app/assets/icons"

SEARCH_USER_ICON = os.path.join(MAIN_ICONS_PATH, "search_user.png")
CANCEL_USER_ICON = os.path.join(MAIN_ICONS_PATH, "cancel_user.png")
AVATAR_USER_ICON = os.path.join(MAIN_ICONS_PATH, "avatar_user.png")