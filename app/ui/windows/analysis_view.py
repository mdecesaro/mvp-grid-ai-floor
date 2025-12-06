import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io

from PIL import Image

class AnalysisView(ctk.CTkToplevel):
    def __init__(self, root, controller=None):
        super().__init__(root)
        self.title("Athlete Performance Analysis")
        self.attributes("-topmost", True)
        self.geometry("1200x700")
        self.resizable(False, False)
        self.controller = controller

    def set_controller(self, controller):
        self.controller = controller

    def build_interface(self):
        # Frames principais
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # === ComboBox para selecionar atleta ===
        self.athlete_var = ctk.StringVar()
        self.athlete_combo = ttk.Combobox(
            self.left_frame, textvariable=self.athlete_var, state="readonly"
        )
        self.athlete_combo.pack(pady=10, padx=10)
        # carregar atletas
        athletes = self.controller.get_all_athletes()
        self.athletes = athletes  # salva para usar depois (pegar ID, etc.)
        self.athlete_combo["values"] = [a.name for a in athletes]
        self.athlete_combo.bind("<<ComboboxSelected>>", self.on_athlete_selected)

        # Placeholder para foto do atleta
        self.photo_label = ctk.CTkLabel(self.left_frame, text="Foto do atleta", width=250, height=250)
        self.photo_label.pack(pady=10)

        # Placeholder para informações pessoais
        self.info_frame = ctk.CTkFrame(self.left_frame)
        self.info_frame.pack(fill="x", pady=10, padx=10)
        self.info_labels = {}
        for attr in ["Name", "Country", "Age", "Height", "Weight", "Position"]:
            lbl = ctk.CTkLabel(self.info_frame, text=f"{attr}: -", anchor="w")
            lbl.pack(fill="x", pady=2)
            self.info_labels[attr] = lbl

        # === Área direita para gráficos e tabela ===
        self.stats_frame = ctk.CTkFrame(self.right_frame)
        self.stats_frame.pack(fill="both", expand=True)

        evaluation = self.controller.get_evaluation_results(1, 1)
        self.create_card(self.stats_frame, "Tempo Médio de Reação", "0.452 s")


        self.figure_frame = ctk.CTkFrame(self.stats_frame)
        self.figure_frame.pack(fill="x", pady=10)

        self.table_frame = ctk.CTkFrame(self.stats_frame)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        
        
    def create_card(self, frame, title, value, width=200, height=100):
        card = ctk.CTkFrame(frame, width=width, height=height, corner_radius=10)
        card.pack_propagate(False)  # mantém tamanho fixo
        card.pack(padx=10, pady=10, anchor="w")

        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="bold"))
        title_label.pack(pady=(10,0))

        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"), text_color="#00ff00")
        value_label.pack(pady=(5,0))
        
        
       

    def on_athlete_selected(self, event):
        selected_atl = self.athlete_var.get()
        athlete = next((a for a in self.athletes if a.name == selected_atl), None)
        if athlete:
            print(f"Athlete selecionado: {athlete.id} - {athlete.name}")
            self.update_profile(athlete)
            self.update_statistics(athlete)

    def update_profile(self, athlete):
        self.info_labels["Name"].configure(text=f"Name: {athlete.name}")
        self.info_labels["Country"].configure(text=f"Country: {athlete.country}")
        self.info_labels["Age"].configure(text=f"Age: {athlete.get_age()}") 
        self.info_labels["Height"].configure(text=f"Height: 1.77m")
        self.info_labels["Weight"].configure(text=f"Weight: 78kg")
        self.info_labels["Position"].configure(text=f"Position: {athlete.position}")

        if hasattr(athlete, "profile") and athlete.profile:
            try:
                img = Image.open(io.BytesIO(athlete.profile))
                img = img.resize((250, 250))  # ajusta ao tamanho
                self.photo_img = CTkImage(light_image=img, dark_image=img, size=(250, 250))
                self.photo_label.configure(image=self.photo_img, text="")  # remove texto
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
                self.photo_label.configure(text="Sem foto", image=None)
        else:
            self.photo_label.configure(text="Sem foto", image=None)
       

    def update_statistics(self, athlete_name):
        # Aqui você pode atualizar os gráficos e tabela com os dados do atleta
        pass

