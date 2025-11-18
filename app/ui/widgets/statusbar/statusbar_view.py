import customtkinter as ctk

class StatusBarWidget(ctk.CTkFrame):
    def __init__(self, parent_frame):
        super().__init__(parent_frame, fg_color="#444444", height=40, corner_radius=0)
        self.pack(fill="x", side="bottom")
        self.pack_propagate(False)
        
        self. _create_fields()
    
    def set_controller(self, controller):
        self.controller = controller

    def _create_fields(self):
        # Botão de status
        self.status_button = ctk.CTkButton(
            self, text="🔴", width=30, height=30,
            fg_color="#444444", text_color="white", hover_color="#555555",
            corner_radius=4,
            command=lambda: self.controller.open_input_selector() if self.controller else None,
            font=("Arial", 18)
        )
        self.status_button.place(x=5, y=5)
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            self, text="No device connected",
            text_color="white", anchor="w"
        )
        self.status_label.place(x=40, y=5)
        
        # Botão desconectar
        self.disconn_button = ctk.CTkButton(
            self, text="x", width=30, height=30, text_color="white",
            fg_color="transparent", hover_color="#A94442",
            command=lambda: self.controller.device_disconnect() if self.controller else None,
            font=("Arial", 18)
        )
        self.disconn_button.place(x=0, y=5)  # posição inicial provisória
        self.disconn_button.place_forget()  # some inicialmente

    def _on_resize(self):
        width = self.winfo_width()
        x_pos = max(width - 40, 5)
        self.disconn_button.place(x=x_pos, y=5)

    def update_status(self, status, device="GRID_AI PRO", version="1.0.0", sensor_count=32):
        if status == "usb":
            self.status_button.configure(fg_color="#339966", text="🟢")
            self.configure(fg_color="#339966")
            self.status_label.configure(text=f"Successfully connected to Arduino. ({device} : {version} : {sensor_count} sensors).")
            self.disconn_button.place() 
            self._on_resize()
        elif status == "mouse":
            self.status_button.configure(fg_color="#339966", text="🟢")
            self.configure(fg_color="#339966")
            self.status_label.configure(text=f"Mouse mode activated. ({device} : {version} : {sensor_count} sensors).")
            self.disconn_button.place()
            self._on_resize()
        elif status == "disconn":
            self.status_button.configure(fg_color="#444444", text="🔴")
            self.configure(fg_color="#444444")
            self.status_label.configure(text="No device connected.")
            self.disconn_button.place_forget()
        else:
            self.status_button.configure(fg_color="#A94442", text="🔴")
            self.configure(fg_color="#A94442")
            self.status_label.configure(text="Device did not respond.")
            self.disconn_button.place_forget()
