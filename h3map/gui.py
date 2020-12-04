import tkinter as tk
from tkinter import Grid
from tkinter.filedialog import askopenfilenames

from h3map.controller import MainController
from h3map.view.view import NameView, DescriptionView, MapsView


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

        self.load = tk.Button(self, text="Load maps", command=self._load)
        self.load.grid(row=0, column=0)

        self.filter = tk.Button(self, text="Filter", command=self.filter)
        self.filter.grid(row=0, column=1)

        self.clear = tk.Button(self, text="Clear", command=self.clear)
        self.clear.grid(row=0, column=2)

        # Filters
        self.selected_size = tk.StringVar()
        self.selected_size.set("XL")
        size = tk.OptionMenu(self, self.selected_size, "XL", "L", "M", "S")
        size.grid(row=0, column=3)

        self.number_of_teams = tk.Entry(self)
        self.number_of_teams.grid(row=0, column=4)

        self.team_size = tk.Entry(self)
        self.team_size.grid(row=0, column=5)

        label_win_condition = tk.Label(self, textvariable="Select win condition")
        label_win_condition.grid(row=0, column=6)
        self.selected_win_condition = tk.StringVar()
        self.selected_win_condition.set(None)
        self.win_condition = tk.OptionMenu(self, self.selected_win_condition,
                             "Standard win",
                             "Acquire artifact",
                             "Accumulate creatures",
                             "Accumulate resources",
                             "Upgrade town",
                             "Build grail",
                             "Defeat hero",
                             "Capture town",
                             "Defeat monster",
                             "Flag creatures",
                             "Flag mines",
                             "Transport artifact",
                             )
        self.win_condition.grid(row=0, column=6)

        label_loss_condition = tk.Label(self, textvariable="Select win condition")
        label_loss_condition.grid(row=0, column=7)
        self.selected_loss_condition = tk.StringVar()
        self.selected_loss_condition.set(None)
        self.loss_condition = tk.OptionMenu(self, self.selected_loss_condition, "Standard loss", "Lose town", "Lose hero",
                             "Time expires")
        self.loss_condition.grid(row=0, column=7)

        #

        panes = tk.PanedWindow(self)
        panes.grid(row=1, columnspan=8, sticky=tk.N + tk.S + tk.E + tk.W)

        self.number_of_maps_loaded = tk.StringVar()
        self.number_of_maps_loaded.set("Maps found: 0")
        label = tk.Label(self, textvariable=self.number_of_maps_loaded)
        label.grid(row=2, column=0)

        self.maps_view = tk.Listbox(panes)

        self.v = tk.StringVar()
        self.map_detail_view = tk.Text(panes, height=2)
        self.maps_view.bind('<<ListboxSelect>>', self.onclick)

        panes.add(self.maps_view, stretch="always")
        panes.add(self.map_detail_view, stretch="always")

    def _load(self):
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
            self.maps_view.insert(1, name.render())

    def update_map_detail(self, description):
        self.map_detail_view.config(state=tk.NORMAL)
        self.map_detail_view.delete("1.0", tk.END)
        self.map_detail_view.insert(tk.END, description)
        self.map_detail_view.config(state=tk.DISABLED)

    def filter(self):
        controller = MainController()
        maps = controller.filter(
            self.maps.all(),
            self.selected_size.get(),
            self.selected_number_of_teams(),
            self._selected_win_condition(),
            self._selected_loss_condition(),
            self.selected_team_size(),
        )

        self._clear_filter()
        self.update_maps(maps)
        self.update_number_of_maps_found(maps.all())

    def clear(self):
        self.update_maps(self.maps)

    def update_number_of_maps_found(self, maps):
        self.number_of_maps_loaded.set("Maps found: {0}".format(len(maps)))

    def selected_number_of_teams(self):
        selected = self.number_of_teams.get()
        if selected == '':
            return None;

        return int(selected)

    def selected_team_size(self):
        selected = self.team_size.get()
        if selected == '':
            return None;

        return int(selected)

    def _selected_win_condition(self):
        selected = self.selected_win_condition.get()
        if selected == 'None':
            return None

        return selected

    def _selected_loss_condition(self):
        selected = self.selected_loss_condition.get()
        if selected == 'None':
            return None

        return selected

    def _clear_filter(self):
        self.maps_view.delete(1, tk.END)

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
