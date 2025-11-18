class WidgetManager:
    def __init__(self, parent_frame, context):
        self.parent = parent_frame
        self.context = context
        self.widgets = {}
        
    def register(self, name, view, controller, row=0, col=0, sticky="nsew", rowspan=1, columnspan=1):
        self.widgets[name] = {"view": view, "controller": controller}
        view.grid(row=row, column=col, sticky=sticky, rowspan=rowspan, columnspan=columnspan, padx=7, pady=7)
    
    def register_status_bar(self, name, view, controller):
         self.widgets[name] = {"view": view, "controller": controller}
                 
    def get_widget(self, name):
        return self.widgets.get(name)

    def get_widget_view(self, name):
        return self.widgets.get(name, {}).get("view")

    def get_widget_controller(self, name):
        return self.widgets.get(name, {}).get("controller")
