import tkinter as tk
from tkinter import Grid
from tkinter.filedialog import askopenfilenames

from h3map.controller import MainController
from h3map.gui.menubar import MenuBar
from h3map.view.view import NameView, DescriptionView, MapsView


class NumberOfMapsLoadedLabel(tk.Label):
    def __init__(self, master=None):
        self.number_of_maps_loaded = tk.StringVar()
        self.number_of_maps_loaded.set("Maps found: 0")
        super().__init__(master, textvariable=self.number_of_maps_loaded)
        self.grid(row=2, column=0)

    def update(self, maps):
        self.number_of_maps_loaded.set("Maps found: {0}".format(len(maps)))


class MapDetailText(tk.Text):
    def __init__(self, master=None):
        self.v = tk.StringVar()
        super().__init__(master, height=2)

    def update(self, description):
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert(tk.END, description)
        self.config(state=tk.DISABLED)


class MapListbox(tk.Listbox):
    def __init__(self, master=None, onclick=None):
        super().__init__(master)
        self.bind('<<ListboxSelect>>', onclick)

    def update(self, name):
        if name:
            self.insert(1, name)
        else:
            self.delete(1, tk.END)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.maps = MapsView([])
        self.create_widgets()

    def create_widgets(self):
        Grid.columnconfigure(self, 0, weight=2)
        Grid.columnconfigure(self, 1, weight=2)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=15)

        self.menubar = MenuBar(self)

        panes = tk.PanedWindow(self)
        panes.grid(row=1, columnspan=8, sticky=tk.N + tk.S + tk.E + tk.W)

        self.number_of_maps_found = NumberOfMapsLoadedLabel(self)
        self.maps_list = MapListbox(panes, onclick=self.onclick)
        self.map_detail = MapDetailText(panes)

        panes.add(self.maps_list, stretch="always")
        panes.add(self.map_detail, stretch="always")

    def load(self):
        files = askopenfilenames()

        controller = MainController()
        maps = controller.load(files)

        self._clear_filter()
        self.maps.update(maps)
        self.update_maps(maps)

        first_description = self.maps.descriptions(0)
        self.update_map_detail(first_description.render())
        self.update_number_of_maps_found(self.maps.all())

    def update_maps(self, maps):
        for name in maps.names():
            self.maps_list.update(name.render())

    def update_map_detail(self, description):
        self.map_detail.update(description)

    def update_number_of_maps_found(self, maps):
        self.number_of_maps_found.update(maps)

    def _clear_filter(self):
        self.maps_list.update(None)

    def clear(self):
        self.update_maps(self.maps)

    def filter(self):
        controller = MainController()
        maps = controller.filter(
            self.maps.all(),
            self.menubar.selected_map_size(),
            self.menubar.selected_team_number(),
            self.menubar.selected_win_condition(),
            self.menubar.selected_loss_condition(),
            self.menubar.selected_player_number(),
        )

        self._clear_filter()
        self.update_maps(maps)
        self.update_map_detail(maps.descriptions(0))
        self.update_number_of_maps_found(maps.all())

    def onclick(self, event):
        w = event.widget
        selection = w.curselection()
        if len(selection):
            idx = int(selection[0])

            description = self.maps.descriptions(idx)
            self.update_map_detail(description.render())

    @classmethod
    def run(cls):
        app = tk.Tk()
        app.title("h3map")
        frame = App(master=app)
        frame.mainloop()


class ReadOnlyText(tk.Text):
    pass