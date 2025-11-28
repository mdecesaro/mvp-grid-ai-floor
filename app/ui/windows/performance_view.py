import customtkinter as ctk
from datetime import datetime

class PerformanceTestingView(ctk.CTkToplevel):
    def __init__(self, master, controller=None):
        super().__init__(master)
        
        self.title("🧪 Performance Testing")
        self.geometry("350x450")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        self.controller = controller

        # Pega dimensões da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Posição e tamanho (metade direita da tela)
        diff = 50
        width = (screen_width // 2) - diff
        height = 500  # altura desejada
        x = (screen_width // 2) + (diff // 2)
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.exercise_combo = None

    def set_controller(self, controller):
        self.controller = controller
        
    def build_interface(self):
        # === Exercício ===
        exercise_frame = ctk.CTkFrame(self)
        exercise_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(exercise_frame, text="Selecione o Exercício:").pack(anchor="w")
        self.exercise_combo = ctk.CTkComboBox(exercise_frame, values=[], command=self._on_exercise_selected)
        self.exercise_combo.pack(fill="x", pady=5)

        self.exercise_details = ctk.CTkTextbox(exercise_frame, height=80, state="disabled")
        self.exercise_details.pack(fill="x", pady=5)

        # === Atleta ===
        athlete_frame = ctk.CTkFrame(self)
        athlete_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(athlete_frame, text="Selecione o Atleta:").pack(anchor="w")
        self.athlete_combo = ctk.CTkComboBox(athlete_frame, values=[])
        self.athlete_combo.pack(fill="x", pady=5)

        # === Botão de iniciar ===
        self.start_btn = ctk.CTkButton(self, text="▶ Iniciar Teste", command=self._start_test)
        self.start_btn.pack(pady=10)

        # === Log ===
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="Log de Execução:").pack(anchor="w")
        self.log_text = ctk.CTkTextbox(log_frame, state="disabled")
        self.log_text.pack(fill="both", expand=True)

    def populate_exercises(self, exercises):
        # Recebe lista de Exercise e coloca no ComboBox
        display_list = [f"{e.name} ({e.category_name}/{e.modality})" for e in exercises]
        self.exercise_map = {display_list[i]: exercises[i] for i in range(len(exercises))}
        self.exercise_combo.configure(values=display_list)
        if display_list:
            self.exercise_combo.set(display_list[0])
            self._show_exercise_details(display_list[0])

    def populate_athletes(self, athletes):
        display_list = [a.name for a in athletes]
        self.athlete_map = {a.name: a for a in athletes}
        self.athlete_combo.configure(values=display_list)
        if display_list:
            self.athlete_combo.set(display_list[0])

    def _on_exercise_selected(self, selection):
        self._show_exercise_details(selection)

    def _show_exercise_details(self, selection):
        exercise = self.exercise_map[selection]
        self.exercise_details.configure(state="normal")
        self.exercise_details.delete("1.0", "end")
        self.exercise_details.insert(
            "1.0",
            f"{exercise.description}\n\nParâmetros:\n{exercise.parameters}"
        )
        self.exercise_details.configure(state="disabled")

    def _start_test(self):
        athlete_name = self.athlete_combo.get()
        exercise_name = self.exercise_combo.get()

        if athlete_name and exercise_name:
            athlete = self.athlete_map[athlete_name]
            exercise = self.exercise_map[exercise_name]
            self.controller.start_evaluation(athlete, exercise)
        else:
            self._log("⚠ Selecione um atleta e um exercício antes de iniciar.")

    def _log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    
