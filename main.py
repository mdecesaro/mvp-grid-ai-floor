import tkinter as tk
import customtkinter as ctk
from app.config.config import DATABASE_PATH, ICON_PATH
from app.context import AppContext
from app.ui.main_ui import AppInterface

def main():
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()

    icon_image = tk.PhotoImage(file=ICON_PATH)
    root.iconphoto(True, icon_image)

    context = AppContext(root, DATABASE_PATH)
    AppInterface(root, context)

    def on_close():
        print("Closing Grid_Ai App...")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    
if __name__ == "__main__":
    main()
