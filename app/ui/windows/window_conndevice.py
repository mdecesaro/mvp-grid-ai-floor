import customtkinter as ctk
import serial.tools.list_ports

class InputDeviceSelector(ctk.CTkToplevel):
    def __init__(self, master, on_select_callback):
        super().__init__(master)
        self.title("Select Source Device")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        self.master = master
        self.on_select_callback = on_select_callback

        modal_width = 380
        modal_height = 180
        x = (self.winfo_screenwidth() - modal_width) // 2
        y = (self.winfo_screenheight() - modal_height) // 2
        self.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        self.lbl_device = ctk.CTkLabel(self, text="Select USB Device or Use Mouse")
        self.lbl_device.place(x=40, y=20)

        self.device_var = ctk.StringVar()
        self.device_list = self.get_serial_ports()
        self.dropdown = ctk.CTkOptionMenu(self, variable=self.device_var, values=self.device_list or ["No USB devices found"])
        self.dropdown.place(x=40, y=60)

        self.btn_usb = ctk.CTkButton(self, text="Use Usb", command=self.use_usb)
        self.btn_usb.place(x=40, y=110)

        self.btn_mouse = ctk.CTkButton(self, text="Use Mouse", command=self.use_mouse)
        self.btn_mouse.place(x=200, y=110)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=5)

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def use_usb(self):
        selected = self.device_var.get()
        if selected and "No USB" not in selected:
            self.on_select_callback(mode="usb", port=selected)
            self.destroy()

    def use_mouse(self):
        self.on_select_callback(mode="mouse", port=None)
        self.destroy()

    

    
