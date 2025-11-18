import customtkinter as ctk

from app.config.config import SEARCH_USER_ICON, CANCEL_USER_ICON, AVATAR_USER_ICON
from app.helpers.image_utils import open_icon_png, create_rounded_rect_photo  
import tkinter as tk

class ProfileWidget(ctk.CTkFrame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._build_ui()

    def _build_ui(self):
        self.configure(
            fg_color="#444444",
            corner_radius=10,
            border_color="#888888",
            border_width=1
        )
        
        btn_search_user = ctk.CTkButton(
            master=self,
            image=open_icon_png(SEARCH_USER_ICON),text="", 
            width=30,height=30,
            fg_color="#333333",hover_color="#555555",
            corner_radius=5,command=lambda: self.controller.load_athlete()
        )
        btn_search_user.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
       
        btn_remove_user = ctk.CTkButton(
            master=self,
            image=open_icon_png(CANCEL_USER_ICON),text="", 
            width=30,height=30,
            fg_color="#333333",hover_color="#555555",
            corner_radius=5,command=lambda: self.controller.clear_athlete()
        )
        btn_remove_user.place(relx=0.0, rely=1.0, anchor="sw", x=60, y=-10)
        
        photo = open_icon_png(AVATAR_USER_ICON, size=(60, 60))
        self.avatar_label = ctk.CTkLabel(self, image=photo, text="", bg_color="#444444")
        self.avatar_label.image = photo
        self.avatar_label.place(relx=0.5, rely=0.4, anchor="center")  # mais acima
        self.alt_widget_text = ctk.CTkLabel(self, text="Select a player", font=("Verdana", 19), text_color="#00FFAA")
        self.alt_widget_text.place(relx=0.5, rely=0.6, anchor="center")  # logo abaixo

        self.photo_label = tk.Label(self, bg="#444444")
        self.photo_label.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

        self.atl_name = ctk.CTkLabel(self, text="", font=("Verdana", 19), text_color="#00FFAA")
        self.atl_name.place(x=107, y=14)

        self.atl_birth_country = ctk.CTkLabel(self, text="", font=("Verdana", 14), text_color="#00FFAA")
        self.atl_birth_country.place(x=107, y=40)

        self.atl_position = ctk.CTkLabel(self, text="", font=("Verdana", 14), text_color="#00FFAA")
        self.atl_position.place(x=107, y=63)
    
    def clear_fields(self):
        self.avatar_label.place(relx=0.5, rely=0.4, anchor="center")
        self.alt_widget_text.place(relx=0.5, rely=0.6, anchor="center")     

        self.photo_label.configure(image="")
        self.photo_label.image = None

        self.atl_name.configure(text="")
        self.atl_position.configure(text="")
        self.atl_birth_country.configure(text="")

    def calculate_width(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        vertical_separator = ctk.CTkFrame(self, width=1, height=self.height-40, fg_color="#888888")
        vertical_separator.place(x=self.width//2, y=20)
        
    def set_controller(self, controller):
        self.controller = controller

    def display_profile(self, athlete):
        self.alt_widget_text.place_forget()
        self.avatar_label.place_forget()

        photo = create_rounded_rect_photo(
            image_blob=athlete.profile, 
            size=(80, 80), 
            corner_radius=8, 
            border_color="#00FFAA", 
            border_width=2
        )
        self.photo_label.configure(image=photo)
        self.photo_label.image = photo

        self.atl_name.configure(text=athlete.name)
        self.atl_position.configure(text=athlete.position)
        self.atl_birth_country.configure(text=athlete.birth + " - " + athlete.country)