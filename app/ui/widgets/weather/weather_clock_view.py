
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageEnhance
import io

class WeatherClockWidget(ctk.CTkCanvas):
    def __init__(self, parent_frame, width=231, height=239):
        super().__init__(parent_frame,
                         width=width,
                         height=height,
                         bg="#2c2c3a",
                         highlightthickness=0)

        self.controller = None
        self.radius = 10
        self.image_id = None
        self.tk_image = None
        self.tk_icon = None

        self.after(100, self._init_fields)

    def set_controller(self, controller):
        self.controller = controller

    def _init_fields(self):
        self.city = self.create_text(20, 27, text="", fill="white", font=("Verdana", 18), anchor="w")
        self.day = self.create_text(23, 57, text="", fill="white", font=("Verdana", 12), anchor="w")
        self.date = self.create_text(18, 210, text="", fill="white", font=("Verdana", 12), anchor="w")
        self.temperature = self.create_text(65, 165, text="", fill="white", font=("Verdana", 23), anchor="w")
        self.condition = self.create_text(115, 125, text="", fill="white", font=("Verdana", 10), anchor="center")

        if self.controller:
            self.controller.start()

    def update_clock(self, time_str, day_of_week, city):
        self.itemconfig(self.city, text=city)
        self.itemconfig(self.day, text=day_of_week)
        self.itemconfig(self.date, text=time_str)

    def update_weather(self, temperature, condition, icon_img_path, icon_code):
        self.itemconfig(self.temperature, text=temperature)
        self.itemconfig(self.condition, text=condition)

        if icon_img_path:
            try:
                from app.config.config import IMGS_WEATHER_WIDGET
                from pathlib import Path
                path = Path(IMGS_WEATHER_WIDGET) / f"{icon_code}.png"
                icon_img = Image.open(path).convert("RGBA")
                icon_img = icon_img.resize((80, 85), Image.LANCZOS)
                self.tk_icon = ImageTk.PhotoImage(icon_img)
                self.create_image(75, 50, image=self.tk_icon, anchor="nw")
            except Exception as e:
                print(f"[Erro ao carregar ícone]: {e}")

        self.load_background(icon_img_path)

    def load_background(self, img_path):
        try:
            with open(img_path, "rb") as f:
                image_data = f.read()
            image_stream = io.BytesIO(image_data)
            pil_img = Image.open(image_stream).convert("RGBA")

            canvas_width = self.winfo_width()
            canvas_height = self.winfo_height()

            pil_img = pil_img.resize((canvas_width, canvas_height), Image.LANCZOS)
            pil_img = self._round_corners(pil_img, self.radius)

            enhancer = ImageEnhance.Brightness(pil_img)
            darker_image = enhancer.enhance(0.8)

            self.tk_image = ImageTk.PhotoImage(darker_image)

            if self.image_id:
                self.itemconfig(self.image_id, image=self.tk_image)
            else:
                self.image_id = self.create_image(0, 0, image=self.tk_image, anchor="nw")
                self.tag_lower(self.image_id)
        except Exception as e:
            print(f"[Erro ao carregar imagem de fundo]: {e}")

    def _round_corners(self, img, radius):
        rounded = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(rounded)
        draw.rounded_rectangle((0, 0, img.size[0] - 3, img.size[1] - 3), radius=radius, fill=255)
        img.putalpha(rounded)
        return img
