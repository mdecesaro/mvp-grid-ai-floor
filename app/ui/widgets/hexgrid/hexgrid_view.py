from PIL import Image, ImageTk
import customtkinter as ctk
import math

class HexGridWidget(ctk.CTkCanvas):
    def __init__(self, parent_frame):
        super().__init__(parent_frame, bg="#1f1f2e", highlightthickness=0)
    
    def draw_canvas_hexgrid(self, device_layout):
        self.device_layout = device_layout

        self._load_background_image()
        self._create_canvas()
        self._draw_hex_grid()

        self.bind("<Button-1>", self._on_canvas_click)

    def get_sensor_by_id(self, sensor_id):
        if 1 <= sensor_id <= len(self.device_layout.sensors):
            return self.device_layout.sensors[sensor_id - 1]
        return None
    
    def len_sensors(self):
        return len(self.device_layout.sensors)
    
    def _load_background_image(self):
        try:
            original_image = Image.open(self.device_layout.layout_image)
            original_image.thumbnail(self.device_layout.thumbnail_image, Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(original_image)
        except Exception as e:
            print(f"[Erro] ao carregar imagem de fundo: {e}")
            self.bg_image = None
    
    def _create_canvas(self):
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        if self.bg_image:
            self.image = self.bg_image
            self.create_image(self.device_layout.image_x, self.device_layout.image_y, anchor="nw", image=self.bg_image)
    
    def _draw_hex_grid(self):
        for sensor in self.device_layout.sensors:
            rect_width = 35
            rect_height = 6

            offset_x = 100
            offset_y = 74
            
            sensor.rect_id = self.create_rectangle(
                sensor.x - rect_width/2 + offset_x,  # esquerda
                sensor.y - rect_height/2 + offset_y, # topo
                sensor.x + rect_width/2 + offset_x,  # direita
                sensor.y + rect_height/2 + offset_y, # baixo
                fill="gray",
                outline="gray"
            )
            sensor.hex_id = self.draw_hex(sensor.x + 100, sensor.y + 100, 48, "")         
            
    def draw_hex(self, x, y, size, fill="", outline="white"):
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.extend((px, py))
        return self.create_polygon(points, fill=fill, outline=outline, tags="hex")
    
    def reset_canvas(self):
        self.delete("all")
    
    def _on_canvas_click(self, event):
        clicked_item = self.find_closest(event.x, event.y)[0]
        for sensor in self.device_layout.sensors:
            if sensor.hex_id == clicked_item:
                self.itemconfig(sensor.rect_id, fill="gray")
                sensor.status = 0
                if hasattr(self, "on_sensor_click") and callable(self.on_sensor_click):
                    self.on_sensor_click(sensor.id)
                break

    def turn_on(self, sensor_id: int, color: str = "#5CE65C"):
        sensor = self.device_layout.sensors[sensor_id - 1]
        self.itemconfig(sensor.rect_id, fill="#5CE65C")
        sensor.status = 1
        
    def turn_off(self, sensor_id: int):
        sensor = self.device_layout.sensors[sensor_id - 1]
        self.itemconfig(sensor.rect_id, fill="gray")
        sensor.status = 0

  
    
    
    

    
    
   