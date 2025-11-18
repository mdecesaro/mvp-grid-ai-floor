import customtkinter as ctk
from tkinter import ttk
import json
import ast

class ExerciceView(ctk.CTkToplevel):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.title("Exercises")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.controller = controller

        modal_width = 1000
        modal_height = 600
        x = (self.winfo_screenwidth() - modal_width) // 2
        y = (self.winfo_screenheight() - modal_height) // 2
        self.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        # Layout geral
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

    def set_controller(self, controller):
        self.controller = controller
    
    def build_form(self):
        self.left_frame.grid_columnconfigure((0, 1), weight=1)
        self.inputs = {}
        labels_and_fields = [
            ("Code", "code"),
            ("Name", "name"),
            ("Description", "description"),
            ("Objective", "objective"),
            ("Category", "category_id"),
            ("Modality", "modality"),
            ("Level", "level"),
            ("Grid_Ai", "board_size"),
        ]

        MODALITY_OPTIONS = [
            "Single-Touch",      # um estímulo por vez
            "Multi-Touch",       # vários estímulos simultâneos
            "Sequence",          # seguir uma sequência predefinida
            "Timed",             # realizar o máximo de ações dentro de um tempo
            "Challenge"          # modo competitivo ou pontuação especial
        ]

        for i, (label, key) in enumerate(labels_and_fields):
            col = 0 if i % 2 == 0 else 1
            row = i // 2

            lbl = ctk.CTkLabel(self.left_frame, text=label)
            lbl.grid(row=row*2, column=col, padx=5, pady=(5, 0), sticky="w")

            if key == "modality":
                entry = ctk.CTkComboBox(self.left_frame, values=MODALITY_OPTIONS)
                entry.set(MODALITY_OPTIONS[0])

            elif key == "category_id":
                try:
                    categories = self.controller.get_categories()  # [(1, "Cognitive"), (2, "Performance"), ...]
                except AttributeError:
                    categories = []  # caso controller ainda não esteja definido
                category_names = [name for _, name in categories]
                entry = ctk.CTkComboBox(self.left_frame, values=category_names if category_names else ["No categories"])
                if category_names:
                    entry.set(category_names[0])
                else:
                    entry.set("No categories")
                self.category_map = {name: cid for cid, name in categories}

            elif key == "board_size":
                board_options = {"Pro - 32": 32, "Home - 14": 14}
                entry = ctk.CTkComboBox(self.left_frame, values=list(board_options.keys()))
                entry.set("Pro")
                self.board_map = board_options

            else:
                entry = ctk.CTkEntry(self.left_frame)

            entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10), sticky="ew")
            self.inputs[key] = entry

        # Parameters (campo de texto maior)
        param_label = ctk.CTkLabel(self.left_frame, text="Parameters (JSON):")
        param_label.grid(row=10, column=0, columnspan=2, sticky="w", padx=5)

        self.param_textbox = ctk.CTkTextbox(self.left_frame, height=100)
        self.param_textbox.grid(row=11, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.inputs["parameters"] = self.param_textbox

        # Botão de salvar
        save_button = ctk.CTkButton(self.left_frame, text="Salvar Exercício", command=lambda: self.save_exercise())
        save_button.grid(row=12, column=0, columnspan=2, pady=10)

    def build_table(self):
        self.tree = ttk.Treeview(
            self.right_frame,
            columns=("Code", "name", "Category", "Modality", "Grid_Ai", "Level"),
            show="headings",
            height=20
        )
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Cabeçalhos e largura das colunas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=110, anchor="center")

        self.controller.load_exercises()

    def on_row_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = self.tree.item(selected[0])["values"][0] 
        self.controller.load_exercise_into_form(item_id)

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def fill_form(self, exercise):
        for key, widget in self.inputs.items():
            value = getattr(exercise, key, "")

            # Campo de texto grande (parameters)
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
                widget.insert("1.0", value if value is not None else "")

            # ComboBox de categoria
            elif key == "category_id" and isinstance(widget, ctk.CTkComboBox):
                inv_map = {v: k for k, v in self.category_map.items()}
                cat_name = inv_map.get(value, "")
                widget.set(cat_name)

            # ComboBox de modalidade
            elif key == "modality" and isinstance(widget, ctk.CTkComboBox):
                widget.set(value if value else (widget.cget("values")[0] if widget.cget("values") else ""))

            # ComboBox de board_size (pro / home)
            elif key == "board_size" and isinstance(widget, ctk.CTkComboBox):
                inv_map = {v: k for k, v in self.board_map.items()}
                board_name = inv_map.get(value, "")
                widget.set(board_name)

            # Campo de entrada padrão (Entry)
            else:
                widget.delete(0, "end")
                widget.insert(0, str(value) if value is not None else "")

        # Guardar ID para saber se é edição
        self.current_exercise_id = exercise.id

    
    def insert_into_table(self, exercises):
        self.tree.delete(*self.tree.get_children())
        for exercise in exercises:
            board_size = getattr(exercise, "board_size", None)
            board_text = (
                "Pro - 32" if board_size == 32
                else "Home - 14" if board_size == 14
                else "Unknown"
            )

            self.tree.insert("", "end", values=(
                exercise.code,
                exercise.name,
                exercise.category_name,
                exercise.modality,
                board_text,
                exercise.level
            ))

    def get_form_data(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                data[key] = widget.get("1.0", "end").strip()
            else:
                data[key] = widget.get().strip()
        return data

    def clear_form(self):
        for key, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")

            elif isinstance(widget, ctk.CTkComboBox):
                # Se for o campo board_size, reseta para "Pro"
                if key == "board_size":
                    widget.set("Pro")
                # Se for outro combobox, reseta para o primeiro valor
                elif widget.cget("values"):
                    widget.set(widget.cget("values")[0])
                else:
                    widget.set("")

            else:  # Entry
                widget.delete(0, "end")


    def save_exercise(self):
        try:
            raw_params = self.inputs["parameters"].get("1.0", "end").strip()
            # Tenta interpretar como dict Python e converter para JSON válido
            try:
                python_dict = ast.literal_eval(raw_params)  # converte string Python para dict
                raw_params = json.dumps(python_dict)        # converte dict para JSON válido
            except (ValueError, SyntaxError):
                try:
                    json_obj = json.loads(raw_params)       # tenta interpretar direto como JSON
                    raw_params = json.dumps(json_obj)       # formata JSON (aspas duplas etc.)
                except json.JSONDecodeError:
                    print("⚠️ Parameters inválido, substituindo por {}")
                    raw_params = "{}"

            data = {
                "id": getattr(self, "current_exercise_id", None),
                "category_id": self.category_map.get(self.inputs["category_id"].get()),
                "code": self.inputs["code"].get().strip(),
                "name": self.inputs["name"].get().strip(),
                "description": self.inputs["description"].get().strip(),
                "level": int(self.inputs["level"].get() or 1),
                "objective": self.inputs["objective"].get().strip(),
                "modality": self.inputs["modality"].get().strip(),
                "parameters": raw_params,
                "board_size": int(self.board_map.get(self.inputs["board_size"].get()))
            }

            # Cria o objeto Exercise
            from app.data.models.exercise import Exercise
            exercise = Exercise(**data)

            # Decide entre INSERT ou UPDATE
            if exercise.id:
                self.controller.update_exercise(exercise)
            else:
                self.controller.add_exercise(exercise)
            
            self.controller.load_exercises()
            self.clear_form()

            print(f"✅ Exercício {'atualizado' if exercise.id else 'criado'} com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar exercício: {e}")
