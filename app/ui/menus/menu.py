import tkinter as tk

class Menu:
    def __init__(self, root):
        self.root = root

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Athletes Menu
        self.athlete_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Athletes", menu=self.athlete_menu)
        
        # Athletes Menu #
        self.diagnosis_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Evaluation Suite", menu=self.diagnosis_menu)
        
    def add_athlete_command(self, label, command):
        self.athlete_menu.add_command(label=label, command=command)

    def add_exercise_command(self, label, command):
        self.diagnosis_menu.add_command(label=label, command=command)

   