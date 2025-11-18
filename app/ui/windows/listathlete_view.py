import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from app.helpers.image_utils import create_rounded_photo

class ListAthleteView(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("List Athletes")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        self.controller = controller

        modal_width = 500
        modal_height = 400
        x = (self.winfo_screenwidth() - modal_width) // 2
        y = (self.winfo_screenheight() - modal_height) // 2
        self.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        self._build_interface()
        self.load_athletes()
       
    def set_controller(self, controller):
        self.controller = controller

    def _build_interface(self):
        # === Estilo Treeview ===
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=50)

        # === Frame principal ===
        main_frame = ctk.CTkFrame(self, fg_color="#1e1e2f", corner_radius=0)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.columns = [('name', 'Name', 180), ('age', 'Age', 70), ('position', 'Position', 150)]
        
        # === Tabela com show='tree headings' para habilitar imagem ===
        self.table = ttk.Treeview(main_frame,
                         columns=[col[0] for col in self.columns],
                         show='tree headings', style="Custom.Treeview")
        self.table.pack(side="top", anchor="n", fill="x")
        self.table.configure(cursor="hand2") 
        self.table.bind("<<TreeviewSelect>>", self._on_athlete_selected)
        
        # Configurar coluna #0 como 'image'
        self.table.column("#0", width=60, anchor="center")
        self.table.heading("#0", text="Image")

        # Configurar as outras colunas normalmente
        for col_id, _, col_width in self.columns:
            self.table.column(col_id, width=col_width, anchor="center")
            self.table.heading(col_id, text=col_id.capitalize())
    
    # === Exemplo de dados ===
    def load_athletes(self):
        atl_list = self.controller.get_athletes()
        self.image_refs = []
        
        for idx, athlete in enumerate(atl_list):
            if athlete.profile:
                photo = create_rounded_photo(athlete.profile)
            else:
               photo = None

            self.image_refs.append(photo)
            data = (
                athlete.name,
                athlete.get_age(),
                athlete.position
            )
            self.table.insert("", "end", iid=str(athlete.id), values=data, image=photo)
        

    def bind_selection_callback(self, callback):
        self.selection_callback = callback

    def _on_athlete_selected(self, event):
        athlete_id = self.table.focus()
        if athlete_id:
            self.controller.athlete_selected(athlete_id)        
