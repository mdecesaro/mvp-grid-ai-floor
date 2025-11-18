import customtkinter as ctk

class LeftFrame(ctk.CTkFrame):
    def __init__(self, root, context):
        super().__init__(root)
        self.root = root
        self.context = context

        # Dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

         # Configura este frame como metade direita da tela
        self.configure(
            width=screen_width // 2,
            height=screen_height,
            fg_color="#1f1f2e",
            corner_radius=0
        )
        self.place(relx=0, rely=0, relwidth=0.5, relheight=1)

         # Habilita layout interno para uso de .grid()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
