import tkinter as tk
from tkinter import Grid
from tkinter.filedialog import askopenfilenames

from h3map.controller import MainController


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.maps = {}
        self.create_widgets()

    def create_widgets(self):
        Grid.columnconfigure(self, 0, weight=2)
        Grid.columnconfigure(self, 1, weight=2)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=15)

        self.load = tk.Button(self, text="Load maps", command=self._load)
        self.load.grid(row=0, column=0)

        self.var = tk.StringVar()
        self.var.set("XL")
        self.size = tk.OptionMenu(self, self.var, "XL", "L", "M", "S")
        self.size.grid(row=0, column=2)

        self.filter = tk.Button(self, text="Filter", command=self.filter_size)
        self.filter.grid(row=0, column=1)

        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.grid(row=0, column=3)

        panes = tk.PanedWindow(self)
        panes.grid(row=1, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

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

        for header in maps.values():
            self.maps[header.metadata.description.name] = header
            self.maps_view.insert(1, header.metadata.description.name)

        self.v.set(list(maps.values())[0])

    def filter_size(self):
        controller = MainController()
        maps = controller.filter(self.maps, self.var.get())

        self.maps_view.delete(1, tk.END)
        for header in maps:
            self.maps_view.insert(1, header.metadata.description.name)

    def onclick(self, event):
        w = event.widget
        selection = w.curselection()
        if len(selection):
            idx = int(selection[0])
            value = w.get(idx)
            self.map_detail_view.config(state=tk.NORMAL)
            self.map_detail_view.delete("1.0", tk.END)
            self.map_detail_view.insert(tk.END, self.maps[value])
            self.map_detail_view.config(state=tk.DISABLED)

    @classmethod
    def run(cls):
        app = tk.Tk()
        app.title("h3map")
        frame = App(master=app)
        frame.mainloop()
