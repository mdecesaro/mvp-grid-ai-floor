import tkinter as tk
from app.ui.widgets.hexgrid.hexgrid_view import HexGridWidget
from app.ui.widgets.hexgrid.hexgrid_controller import HexGridController


class LeftFrameController:
    def __init__(self, context, left_frame):
        self.context = context
        self.left_frame = left_frame

        self._init_widgets()

    def _init_widgets(self):
        hexgrid_widget = HexGridWidget(self.left_frame)
        hexgrid_widget.grid(row=0, column=0, sticky="nsew", rowspan=1, columnspan=1, padx=7, pady=7)
        hex_grid_controller = HexGridController(self.context, hexgrid_widget)

        self.context.set_hexgrid(hexgrid_widget, hex_grid_controller)
    
  