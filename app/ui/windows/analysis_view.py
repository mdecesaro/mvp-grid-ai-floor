import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import ttk
#import matplotlib.pyplot as plt
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

        self.stats_frame = None

        self.df_final = None
        self.athlete = None

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

        self.figure_frame = ctk.CTkFrame(self.stats_frame)
        self.figure_frame.pack(fill="x", pady=10)

        # Frame da linha de título colorida
        title_frame = ctk.CTkFrame(
            self.figure_frame,
            fg_color="#2b2b2b",  # cor de fundo da linha de título
            height=30
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)  # mantém altura fixa

        # Label do título centralizado
        title_label = ctk.CTkLabel(
            title_frame,
            text="Athlete Statistics",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff"  # cor do texto
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        self.table_frame = ctk.CTkFrame(self.stats_frame)
        self.table_frame.pack(fill="both", expand=True, pady=10)

    def on_athlete_selected(self, event):
        selected_atl = self.athlete_var.get()
        self.athlete = next((a for a in self.athletes if a.name == selected_atl), None)
        if self.athlete:
            self.update_profile()
            #self.update_statistics()
            self.load_athlete_dataset()

    def load_athlete_dataset(self):
        self.df = self.controller.get_evaluation_results(self.athlete.id)
       
        rs_m = self.reaction_stats(self.df)
        rt_status = self.controller.compare_adaptive_window(self.df)
        
        self.create_custom_card(
            frame=self.figure_frame,
            width=180,
            height=145,
            title="TRT",
            left_value=rs_m["mean_rt"],
            right_top=rs_m["median_rt"],
            right_bottom=rs_m["std_rt"],
            footer=int(rt_status["improvement_percent"]),
            trend=rt_status["trend"]
        )
        

    def create_custom_card(self, frame, width, height, title="", left_value="", right_top="", right_bottom="", footer="", trend=None):
        # ---------------------- Card Base ----------------------
        card = ctk.CTkFrame(frame, width=width, height=height, corner_radius=5, border_color="#282828", border_width=1)
        card.pack(padx=6, pady=6, anchor="w")
        card.pack_propagate(False)

        # ---------------------- Linha 1: Título ----------------------
        titel_frame = ctk.CTkFrame(card, height=30, corner_radius=5)
        titel_frame.pack(fill="x", padx=8, pady=(4, 4))
        titel_frame.pack_propagate(False)

        titel_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            titel_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="center"
        )
        title_label.grid(row=0, column=0, sticky="nsew", padx=(2, 2))

        # ---------------------- Linha 2: Conteúdo ----------------------
        # ---------------------- Linha do meio: grid layout ----------------------
        middle_row = ctk.CTkFrame(card, height=60)
        middle_row.pack(fill="x", expand=True, padx=8)
        middle_row.pack_propagate(False)

       # Configura grid da linha do meio: 1 row, 2 colunas
        middle_row.grid_rowconfigure(0, weight=1)
        middle_row.grid_columnconfigure(0, weight=1)  # Coluna esquerda 50%
        middle_row.grid_columnconfigure(1, weight=1)  # Coluna direita 50%
        
        # Frame interno da coluna esquerda
        left_frame = ctk.CTkFrame(middle_row, fg_color=None)  # transparente
        left_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Configura grid para centralizar verticalmente
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Valor principal
        left_label = ctk.CTkLabel(
            left_frame,
            text=left_value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00ff00",
            fg_color="#2b2b2b",
            corner_radius=5
        )
        left_label.grid(row=0, column=0, sticky="nsew", pady=(0,0))

        # Texto menor
        left_small_label = ctk.CTkLabel(
            left_frame,
            text="ms",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            fg_color="#2b2b2b"
        )
        left_small_label.grid(row=1, column=0, sticky="nsew", pady=(0,0))
        
        # ----------------- Coluna direita (2 linhas internas) -----------------
        # Frame para organizar as duas linhas
        right_frame = ctk.CTkFrame(middle_row, fg_color="#2b2b2b")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Linha superior
        right_top_label = ctk.CTkLabel(
            right_frame,
            text=right_top,
            font=ctk.CTkFont(size=16),
            fg_color="#3a3a3a",
            corner_radius=5,
            text_color="#ffffff"
        )
        right_top_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Linha inferior
        right_bottom_label = ctk.CTkLabel(
            right_frame,
            text=right_bottom,
            font=ctk.CTkFont(size=16),
            fg_color="#3a3a3a",
            corner_radius=5,
            text_color="#ffffff"
        )
        right_bottom_label.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        # ---------------------- Linha 3: Rodapé ----------------------
        footer_frame = ctk.CTkFrame(card, height=30)
        footer_frame.pack(fill="x", padx=8, pady=(4, 6))
        footer_frame.pack_propagate(False)

        # Grid layout
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)
        footer_frame.grid_columnconfigure(2, weight=0)

        if footer is None:
            arrow, color, text = "→", "#adb5bd", "—"
        else:
            if footer > 0:
                arrow, color, text = "↑", "#4CAF50", f"+{footer:.1f}%"
            elif footer < 0:
                arrow, color, text = "↓", "#F44336", f"{footer:.1f}%"
            else:
                arrow, color, text = "→", "#adb5bd", "0.0%"

        # Texto à esquerda
        footer_label = ctk.CTkLabel(
            footer_frame,
            text=f"{arrow} {text}",
            font=ctk.CTkFont(size=13),
            text_color="#adb5bd",
            anchor="center"
        )
        footer_label.grid(row=0, column=0, sticky="nsew", padx=(2, 2))

        # Improvement: seta + percentual
        footer_label_impro = ctk.CTkLabel(
            footer_frame,
            text=trend,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color,
            anchor="center"
        )
        footer_label_impro.grid(row=0, column=1, sticky="nsew", padx=(2, 2))
        
        return card


    def reaction_stats(self, df):
        return {
            "mean": round(df["reaction_time"].mean(), 1),
            "median": round(df["reaction_time"].median(), 1),
            "std": round(df["reaction_time"].std(), 1),
            "mean_rt": round(df["reaction_time_adjusted"].mean(), 1),
            "median_rt": round(df["reaction_time_adjusted"].median(), 1),
            "std_rt": round(df["reaction_time_adjusted"].std(), 1)
        }
    
    def update_profile(self):
        self.info_labels["Name"].configure(text=f"Name: {self.athlete.name}")
        self.info_labels["Country"].configure(text=f"Country: {self.athlete.country}")
        self.info_labels["Age"].configure(text=f"Age: {self.athlete.get_age()}") 
        self.info_labels["Height"].configure(text=f"Height: 1.77m")
        self.info_labels["Weight"].configure(text=f"Weight: 78kg")
        self.info_labels["Position"].configure(text=f"Position: {self.athlete.position}")

        if hasattr(self.athlete, "profile") and self.athlete.profile:
            try:
                img = Image.open(io.BytesIO(self.athlete.profile))
                img = img.resize((250, 250))  # ajusta ao tamanho
                self.photo_img = CTkImage(light_image=img, dark_image=img, size=(250, 250))
                self.photo_label.configure(image=self.photo_img, text="")  # remove texto
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
                self.photo_label.configure(text="Sem foto", image=None)
        else:
            self.photo_label.configure(text="Sem foto", image=None)
       

    def update_statistics(self):
        pass

