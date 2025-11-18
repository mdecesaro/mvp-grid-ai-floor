
from app.controllers.app_controller import AppController
from app.ui.menus.menu import Menu
from app.controllers.menu_controller import MenuController
from app.ui.frames.left_frame import LeftFrame
from app.controllers.left_frame_controller import LeftFrameController
from app.ui.frames.right_frame import RightFrame
from app.controllers.right_frame_controller import RightFrameController

class AppInterface:
    def __init__(self, root, context):
        self.root = root
        self.context = context

        self.root.title("FlyFeet - Grid_Ai")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        # Grid_Ai - Canvas Left Frame 
        self.left_frame = LeftFrame(self.root, self.context)    
        self.left_frame_controller = LeftFrameController(self.context, self.left_frame)

        # Grid_Ai - Dashboard Right Frame
        self.right_frame = RightFrame(self.root, self.context)    
        self.right_frame_controller = RightFrameController(self.context, self.right_frame)
        
        # Menu Bar
        self.menu_view = Menu(self.root)
        self.menu_controller = MenuController(self.menu_view, self.context)
       
        # App Main Controller
        self.app_controller = AppController(self.context, self.left_frame_controller, self.right_frame_controller, self.menu_controller)
        
        

       
    
    
        
    
   
       
    
    """
        self.current_athlete = None
        self.profile_preview_image_id = None
        self.profile_image_data = None
        self.profile_photo = None
    """    
    
        
        
   

       
    """    
    def unbind_sensors(self):
        for sensor in self.hexgrid.sensores:
            sensor.status = 0
            self.canvas.itemconfig(sensor.hex_id, fill="#312F2F")
            self.canvas.tag_unbind(sensor.hex_id, "<Button-1>")
            self.canvas.tag_unbind(sensor.hex_id, "<Enter>")
            self.canvas.tag_unbind(sensor.hex_id, "<Leave>")
            
    def bind_sensors(self):
        for sensor in self.hexgrid.sensores:
            if self.sensor_count == 32:
                sensor.status = 1
                self.canvas.itemconfig(sensor.hex_id, fill="")
                self.canvas.tag_bind(sensor.hex_id, "<Button-1>", lambda e, i=sensor.id: self.on_hex_click(i))
                self.canvas.tag_bind(sensor.hex_id, "<Enter>", lambda e: self.canvas.config(cursor="hand"))
                self.canvas.tag_bind(sensor.hex_id, "<Leave>", lambda e: self.canvas.config(cursor=""))
            elif self.sensor_count == 14:
                if sensor.id not in (1,2,3,4,5,9,10,13,14,19,20,23,24,28,29,30,31,32):
                    sensor.status = 1
                    self.canvas.itemconfig(sensor.hex_id, fill="")
                    self.canvas.tag_bind(sensor.hex_id, "<Button-1>", lambda e, i=sensor.id: self.on_hex_click(i))
                    self.canvas.tag_bind(sensor.hex_id, "<Enter>", lambda e: self.canvas.config(cursor="hand"))
                    self.canvas.tag_bind(sensor.hex_id, "<Leave>", lambda e: self.canvas.config(cursor=""))
    """          
    