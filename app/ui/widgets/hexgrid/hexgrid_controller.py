from app.ui.widgets.hexgrid.hexgrid_view import HexGridWidget
import math
import traceback

class HexGridController:
    def __init__(self, context, view: HexGridWidget):
        self.context = context
        self.view = view
        self.size = 48

        self.device_layout = self.context.device_layout
        
    def update_layout(self, sensor_count):
        print(f"[HexGridController] Atualizando layout com {sensor_count} sensores")
        
        self.device_layout.load_layout(sensor_count)
        self.view.reset_canvas()
        if self.device_layout.is_layout_drawable():
            self._generate_positions()
            self.view.draw_canvas_hexgrid(self.device_layout)
        
    def _generate_positions(self):
        offset_x = 253
        offset_y = 270
    
        w = self.size * 2  
        h = math.sqrt(3) * self.size 

        total_cols = len(self.device_layout.layout)
    
        center_x = 0
        center_y = 0

        total_width = total_cols * (3/4 * w)
        start_x = center_x - total_width / 2 + self.size

        position = 0
        id_sensor = 1
        for col_index, hex_count in enumerate(self.device_layout.layout):
            col_x = start_x + col_index * (3/4 * w)
            col_height = hex_count * h
            start_y = center_y - col_height / 2 + h / 2
            
            for row in range(hex_count):
                x = col_x + offset_x  
                y = start_y + row * h + offset_y
                
                if position not in self.device_layout.excluded_sensors:
                    self.device_layout.sensors[id_sensor-1].x = x
                    self.device_layout.sensors[id_sensor-1].y = y
                    id_sensor += 1
                position += 1
                
               