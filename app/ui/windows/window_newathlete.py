import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import io

class NewAthleteWindow(ctk.CTkToplevel):
    def __init__(self, master, context):
        super().__init__(master)
        self.title("Add New Athlete")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        self.athlete_dao = context.athlete_dao

        modal_width = 600
        modal_height = 340
        x = (self.winfo_screenwidth() - modal_width) // 2
        y = (self.winfo_screenheight() - modal_height) // 2
        self.geometry(f"{modal_width}x{modal_height}+{x}+{y}")
        self.configure(fg_color="#22222f")

        
        form_frame = ctk.CTkFrame(self, fg_color="#22222f", height=280, width=modal_width // 2, corner_radius=0)
        form_frame.place(x=0, y=0)

        # FORM FRAME
        margin_x = 30
        self.input_name = self._add_labeled_entry(form_frame, "Name", x=margin_x+2, y=20, entry_y=50, width=245)
        self.input_name.focus()

        self.input_gender = self._add_labeled_combobox(form_frame, "Gender", ["Male", "Female"],
                                                       x=margin_x+2, y=80, box_x=margin_x, box_y=110, width=115)

        self.input_birth = self._add_labeled_entry(form_frame, "Birth", x=163, y=80, entry_y=110, width=115,
                                                   placeholder="dd/mm/yyyy")
        self.input_birth.bind("<KeyRelease>", self.apply_date_mask)

        self.input_national = self._add_labeled_entry(form_frame, "Country", x=margin_x+2, y=140, entry_y=170, width=115)

        self.input_dominant = self._add_labeled_combobox(form_frame, "Dominant foot", ["Left", "Right"],
                                                         x=163, y=140, box_x=160, box_y=170, width=114)

        position_options = ["Goalkeeper", "Center back", "Right Fullback", "Left Fullback",
                            "Center Midfield", "Right Midfield/Wing", "Left Midfield/Wing", "Forward"]
        self.input_position = self._add_labeled_combobox(form_frame, "Position", position_options,
                                                         x=margin_x+2, y=200, box_x=margin_x, box_y=230, width=245)

        # IMAGE FRAME
        vertical_separator = ctk.CTkFrame(self, width=1, height=260, fg_color="#888888")
        vertical_separator.place(x=((modal_width)//2)+5, y=20)

        image_frame = ctk.CTkFrame(self, fg_color="#22222f", height=280, width=modal_width // 2, corner_radius=0)
        image_frame.place(x=(modal_width//2)+10, y=0)

        canvas_width = (modal_width // 2) - 15
        canvas_height = 180
        self.profile_canvas = ctk.CTkCanvas(image_frame, width=canvas_width, height=canvas_height,
                                            bg="#22222f", highlightthickness=0)
        self.profile_canvas.place(x=0, y=0)

        cx = (canvas_width // 2)
        cy = canvas_height // 2
        radius = 60
        self.profile_canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill="#22222f", outline="white"
        )

        self.profile_preview_image_id = None
        self.profile_photo = None
        self.profile_image_data = None

        upload_btn = ctk.CTkButton(image_frame, text="Profile Avatar",
                                   command=lambda: self.upload_image_callback())
        upload_btn.place(x=75, y=canvas_height)

        self.lbl_saved = ctk.CTkLabel(image_frame, text="", text_color="white")
        self.lbl_saved.place(x=50, y=canvas_height+60)

        save_btn = ctk.CTkButton(self, text="Save", width=200, height=35, command=lambda: self.save())
        save_btn.place(x=(modal_width//2)-(200//2), y=290)

        self.clear_fields()

        

    def _add_labeled_entry(self, parent, label, x, y, entry_y, width, placeholder=""):
        ctk.CTkLabel(parent, text=label, text_color="white").place(x=x, y=y)
        entry = ctk.CTkEntry(parent, width=width, placeholder_text=placeholder)
        entry.place(x=x-2, y=entry_y)
        return entry

    def _add_labeled_combobox(self, parent, label, values, x, y, box_x, box_y, width):
        ctk.CTkLabel(parent, text=label, text_color="white").place(x=x, y=y)
        box = ctk.CTkComboBox(parent, values=values, width=width)
        box.place(x=box_x, y=box_y)
        self.disable_typing(box)
        return box

    def disable_typing(self, widget):
        widget.bind("<Key>", lambda e: "break")

    def apply_date_mask(self, event):
        widget = event.widget
        value = widget.get().replace("/", "")
        new_value = ""

        for i, digit in enumerate(value):
            if i == 2 or i == 4:
                new_value += "/"
            if i < 8 and digit.isdigit():
                new_value += digit

        widget.delete(0, "end")
        widget.insert(0, new_value)

    def save(self):
        try:
            name = self.input_name.get().strip()
            gender = self.input_gender.get().strip()
            birth = self.input_birth.get().strip()
            country = self.input_national.get().strip()
            dominant = self.input_dominant.get().strip()
            position = self.input_position.get().strip()
            profile = self.profile_image_data
            
            if not name or not country or not birth:
                self.lbl_saved.configure(text="All text fields are required! ⚠️")
                print("(1) All text fields are required.")
                return

            id_athlete = self.athlete_dao.insert_athlete(
                name, gender, country, birth, dominant, position, profile
            )

            print(f"Athlete {id_athlete} saved!")
            self.lbl_saved.configure(text="Athlete saved successfully! ✅")

            self.profile_preview_image_id = None
            self.profile_image_data = None
            self.profile_photo = None

            self.clear_fields()
    
        except ValueError:
            self.lbl_saved.configure(text="All text fields are required! ⚠️")
            print("(2) All text fields are required.")

    def clear_fields(self):
        self.input_name.delete(0, "end")
        self.input_gender.set("")
        self.input_birth.delete(0, "end")
        self.input_birth.configure(placeholder_text="dd/mm/yyyy")
        self.input_national.delete(0, "end")
        self.input_dominant.set("")
        self.input_position.set("")

        # Opcional: limpa imagem também
        self.profile_image_data = None
        self.profile_photo = None
        if self.profile_preview_image_id:
            self.profile_canvas.delete(self.profile_preview_image_id)
            self.profile_preview_image_id = None


    def upload_image_callback(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar imagem do atleta",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")],
            parent=self
        )
        self.lift()      
        self.focus_force()
        
        if file_path:
            with open(file_path, "rb") as f:
                self.profile_image_data = f.read()
        else:
            return
        
        image = Image.open(io.BytesIO(self.profile_image_data))
        image = image.resize((120, 120))
        self.profile_photo = ImageTk.PhotoImage(image)

        if not hasattr(self, "profile_canvas"):
            print("Canvas ainda não existe!")
            return

        cx = self.profile_canvas.winfo_width() // 2
        cy = self.profile_canvas.winfo_height() // 2

        circular_image = self.make_circle_image(self.profile_image_data, size=(120, 120))
        self.profile_photo = ImageTk.PhotoImage(circular_image)

        if hasattr(self, "profile_preview_image_id") and self.profile_preview_image_id is not None:
            try:
                self.profile_canvas.itemconfig(self.profile_preview_image_id, image=self.profile_photo)
            except Exception as e:
                print("Erro ao atualizar imagem:", e)
        else:
            self.profile_preview_image_id = self.profile_canvas.create_image(cx, cy, image=self.profile_photo)


    def make_circle_image(self, image_data, size=(120, 120)):
        image = Image.open(io.BytesIO(image_data)).resize(size).convert("RGBA")

        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        result = Image.new("RGBA", size)
        result.paste(image, (0, 0), mask)

        return result

