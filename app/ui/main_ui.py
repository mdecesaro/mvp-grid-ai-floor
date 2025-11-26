
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
