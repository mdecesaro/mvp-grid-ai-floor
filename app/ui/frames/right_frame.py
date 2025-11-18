import customtkinter as ctk

class RightFrame(ctk.CTkFrame):
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
            fg_color="#2c2c3a",
            corner_radius=0
        )
        self.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Desativa expansão automática
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._set_widget_grid_frame()
        
    def _set_widget_grid_frame(self):
        self.widgets_frame = ctk.CTkFrame(self, fg_color="#2c2c3a", corner_radius=0)
        self.widgets_frame.pack(side="top", fill="both", expand=True)

        slot_size = 237
        for row in range(3):
            self.widgets_frame.rowconfigure(row, minsize=slot_size, weight=0)
        for col in range(3):
            self.widgets_frame.columnconfigure(col, minsize=slot_size, weight=0)

