import tkinter as tk


class LoadMapsButton(tk.Button):
    def __init__(self, master=None, onload=None):
        super().__init__(master, text="Load maps", command=onload)
        self.pack(side="left")


class FilterButton(tk.Button):
    def __init__(self, master=None, onfilter=None):
        super().__init__(master, text="Filter", command=onfilter)
        self.pack(side="left")


class ClearButton(tk.Button):
    def __init__(self, master=None, onclear=None):
        super().__init__(master, text="Clear", command=onclear)
        self.pack(side="left")


class SelectSizeOptionMenu(tk.OptionMenu):
    def __init__(self, master=None):
        self.selected_size = tk.StringVar()
        self.selected_size.set("XL")

        super().__init__(master, self.selected_size, "XL", "L", "M", "S")
        self.pack(side="left")

    def selected(self):
        return self.selected_size.get()


class SetNumberOfTeamsEntry(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side="left")

    def selected(self):
        _selected = self.get()
        if _selected == '':
            return None;

        return int(_selected)


class SetTeamSizeEntry(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side="left")

    def selected(self):
        _selected = self.get()
        if _selected == '':
            return None;

        return int(_selected)


class SelectWinConditionOptionMenu(tk.OptionMenu):
    def __init__(self, master=None):
        label_win_condition = tk.Label(master, textvariable="Select win condition")
        label_win_condition.pack(side="left")
        self.selected_win_condition = tk.StringVar()
        self.selected_win_condition.set(None)
        super().__init__(master, self.selected_win_condition,
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
        self.pack(side="left")

    def selected(self):
        _selected = self.selected_win_condition.get()
        if _selected == 'None':
            return None

        return _selected


class SelectLossConditionOptionMenu(tk.OptionMenu):
    def __init__(self, master=None):
        self.label_loss_condition = tk.Label(master, textvariable="Select win condition")
        self.label_loss_condition.pack(side="left")
        self.selected_loss_condition = tk.StringVar()
        self.selected_loss_condition.set(None)
        super().__init__(master, self.selected_loss_condition, "Standard loss", "Lose town",
                         "Lose hero",
                         "Time expires")
        self.pack(side="left")

    def selected(self):
        _selected = self.selected_loss_condition.get()
        if _selected == 'None':
            return None

        return _selected


class MenuBar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, columnspan=2)

        self.load = LoadMapsButton(self, master.load)
        self.filter = FilterButton(self, master.filter)
        self.clear = ClearButton(self, master.clear)
        self.select_size = SelectSizeOptionMenu(self)
        self.number_of_teams = SetNumberOfTeamsEntry(self)
        self.team_size = SetTeamSizeEntry(self)
        self.select_win_condition = SelectWinConditionOptionMenu(self)
        self.select_loss_condition = SelectLossConditionOptionMenu(self)

    def selected_team_number(self):
        self.number_of_teams.selected()

    def selected_map_size(self):
        self.select_size.selected()

    def selected_win_condition(self):
        self.select_win_condition.selected()

    def selected_loss_condition(self):
        self.select_loss_condition.selected()

    def selected_player_number(self):
        self.team_size.selected()


