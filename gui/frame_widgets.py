import math
from tkinter import *
from tkinter import ttk


def shift_coord(coord, column_shift, row_shift=0):
    column, row = coord
    return column + column_shift, row + row_shift


def widget_grid(widget, coord):
    column, row = coord
    widget.grid(column=column, row=row)


def get_col_index(index):
    remainder = index % 3
    return 2 * remainder + 1


def get_row_index(index, offset):
    factor = index // 3
    return 3 * factor + offset


def combine_chromosome_genes(chromosome_list):
    hyperparameter_list = []
    for chromosome in chromosome_list:
        hyperparameter = [chromosome[:3], chromosome[3:6], chromosome[6:]]
        hyperparameter = [" / ".join([str(x) for x in parameter_list]) for parameter_list in hyperparameter]
        hyperparameter_list.append(hyperparameter)
    return hyperparameter_list


class FrameWidgets:
    def __init__(self, root):
        # Create new frame
        self.win = Frame(root)
        # Assign widgets
        self.widgets = {
            "Entry": self.create_entry,
            "SpinBox": self.create_spinbox,
            "OptionMenu": self.create_option_menu,
            "CheckButton": self.create_checkbutton
        }

    def create_gui_frame(self, widget_lists, button_labels):
        # Widget values
        widget_vars = []
        # Row count
        rows = 0
        # Create sections
        for x in range(len(widget_lists)):
            # Unpack section widgets
            label, widget_list = widget_lists[x]
            # Create section and append widget vars
            widget_variables = self.create_gui_section(label, widget_list, rows)
            widget_vars.append(widget_variables)
            # Add number of widgets to total
            num_widget = len(widget_list)
            rows += (num_widget + 1) * 2
        # Add buttons
        button_list = self.add_buttons(button_labels, rows, True)
        # Configure grid rows and columns
        for x in range(5): self.win.grid_columnconfigure(x, weight=1)
        for y in range(rows + 2): self.win.grid_rowconfigure(y, weight=1)
        # Return frame and button list
        return self.win, widget_vars, button_list

    def create_gui_section(self, label, widget_list, row):
        # Number of widgets
        num_widget = len(widget_list)
        # Section label
        self.create_label(label, (2, row))
        # Section lines
        self.vertical_lines(row + 1, [0, 2, 4], num_widget * 2 + 1)
        self.horizontal_lines(range(row + 1, row + (num_widget + 1) * 2, 2), 5)
        # Place widgets
        widget_variables = []
        for index in range(num_widget):
            widget_type, widget_settings = widget_list[index]
            widget_variable = self.widgets[widget_type](*widget_settings, (3, row + (index + 1) * 2))
            widget_variables.append(widget_variable)
        # Return widget list
        return label, widget_variables

    def create_results_frame(self, widget_lists, button_labels):
        # Row count
        rows = 0
        # Create sections
        for x in range(len(widget_lists)):
            # Unpack section widgets
            label, widget_list = widget_lists[x]
            # Create section and append widget vars
            self.create_results_section(label, widget_list, rows)
            # Add number of rows to total
            num_rows = math.ceil(len(widget_list) / 3)
            rows += num_rows * 3 + 2
        # Add buttons
        button_list = self.add_buttons(button_labels, rows, False)
        # Configure grid rows and columns
        for x in range(7): self.win.grid_columnconfigure(x, weight=1)
        for y in range(rows + 2): self.win.grid_rowconfigure(y, weight=1)
        # Return frame and button list
        return self.win, button_list

    def create_results_section(self, label, widget_list, row):
        # Number of rows
        num_rows = math.ceil(len(widget_list) / 3)
        # Section label
        self.create_label(label, (3, row))
        # Section lines
        self.vertical_lines(row + 1, range(0, 7, 2), num_rows * 3 + 1)
        self.horizontal_lines(range(row + 1, row + (num_rows + 1) * 3, 3), 7)
        # Place labels and values
        for index, (widget, value) in enumerate(widget_list):
            # Column and row index
            col_index, row_index = get_col_index(index), get_row_index(index, row + 2)
            # Place labels
            self.create_label(widget, (col_index, row_index))
            # Place values
            self.create_label(value, (col_index, row_index + 1))

    def hyperparameter_results(self, hyperparameter_widgets, fittest_chromosomes, button_labels):
        # Unpack hyperparameter widgets
        label, widget_list = hyperparameter_widgets[0]
        # Create section and append widget vars
        self.create_results_section(label, widget_list, 0)

        # Number of rows and chromosomes
        rows = math.ceil(len(widget_list) / 3) * 3 + 2
        chromosomes = len(fittest_chromosomes)

        # Frame dimensions
        for x in range(7): self.win.grid_columnconfigure(x, weight=1)
        for y in range(rows + chromosomes + 6): self.win.grid_rowconfigure(y, weight=1)

        # Section label
        self.create_label("Hyper-parameters", (3, rows))
        self.place_row_labels(rows + 2, ["Learning Rate", "Explore Rate", "Discount Factor"])

        # Section lines
        self.vertical_lines(rows + 1, range(0, 7, 2), chromosomes + 4)
        self.horizontal_lines([rows + 1, rows + 3, rows + chromosomes + 4], 7)

        # Place hyperparameters from chromosomes
        hyperparameter_list = combine_chromosome_genes(fittest_chromosomes)
        for index, hyperparameter in enumerate(hyperparameter_list):
            self.place_row_labels(rows + index + 4, hyperparameter)

        # Add buttons
        button_list = self.add_buttons(button_labels, rows + chromosomes + 5, False)

        # Return frame and button list
        return self.win, button_list

    def experiment_settings(self, original_results):
        # Frame dimensions
        for x in range(8): self.win.grid_columnconfigure(x, weight=1)
        for y in range(20): self.win.grid_rowconfigure(y, weight=1)

        # Title labels
        self.create_label("Experiment Settings", (3, 0), 2)
        self.create_label("Other Settings", (1, 15))

        # Vertical and Horizontal lines
        self.vertical_lines(1, [0, 2, 7], 17)
        self.horizontal_lines(range(1, 18, 4), 8)

        # Hyper-parameters
        learning_rate = self.triple_spinbox_scale("Learning Rate", 90, 10, 4, (3, 3))
        explore_rate = self.triple_spinbox_scale("Explore Rate", 50, 1, 2, (3, 7))
        discount_factor = self.triple_spinbox_scale("Discount Factor", 90, 99, 1, (3, 11))

        # Other Settings
        confidence = self.single_spinbox_scale("Confidence", (500, 999, 1000), 990, (4, 14))
        new_runs = self.create_spinbox("New Runs", (30, 100, 1), 30, (4, 15), 1)
        mean = self.create_entry("Old Mean", original_results["Mean"], (6, 15), 1)
        old_runs = self.create_spinbox("Old Runs", (30, 100, 1), original_results["Size"], (4, 16), 1)
        std = self.create_entry("Old STD", original_results["STD"], (6, 16), 1)

        # Widget values
        exp_settings = [learning_rate, explore_rate, discount_factor, new_runs, confidence, mean, std, old_runs]
        widget_vars = [("Experiment Settings", exp_settings)]

        # Buttons
        back_button = self.create_button("Back", (3, 18))
        start_button = self.create_button("Start", (4, 18))

        # Return widgets
        return self.win, widget_vars, [back_button, start_button]

    def tune_settings(self):
        # Frame dimensions
        for x in range(8): self.win.grid_columnconfigure(x, weight=1)
        for y in range(15): self.win.grid_rowconfigure(y, weight=1)

        # Title label
        self.create_label("Hyperparameter Settings", (3, 0), 2)

        # Other labels
        self.create_label("Other", (1, 10))
        self.create_label("Settings", (1, 11))
        self.create_label("Rate", (3, 2))
        self.create_label("Rate", (3, 4))

        # Vertical and Horizontal lines
        self.vertical_lines(1, [0, 2, 7], 12)
        self.horizontal_lines(list(range(1, 10, 2)) + [12], 8)

        # Scale Settings
        crossover = self.single_spinbox_scale("Crossover", (0, 100, 100), 75, (4, 2), 5)
        mutation = self.single_spinbox_scale("Mutation", (0, 100, 100), 5, (4, 4), 5)
        single_double = self.double_spinbox_scale("Single / Double", (2, 6))
        roulette_tournament = self.double_spinbox_scale("Tournament / Roulette", (2, 8))

        # Experiment Settings
        population = self.create_spinbox("Population", (10, 100, 2), 10, (4, 10), 1)
        generation = self.create_spinbox("Generation", (1, 100, 1), 50, (4, 11), 1)
        elite = self.create_spinbox("Elite", (0, 10, 2), 2, (6, 10), 1)
        best = self.create_spinbox("Best", (1, 10, 1), 10, (6, 11), 1)

        # Widget values
        tune_settings = [crossover, mutation, single_double, roulette_tournament, population, generation, elite, best]
        widget_vars = [("Hyperparameter Settings", tune_settings)]

        # Buttons
        back_button = self.create_button("Back", (3, 13))
        start_button = self.create_button("Start", (4, 13))

        # Return widgets
        return self.win, widget_vars, [back_button, start_button]

    def add_buttons(self, labels, row, gui):
        # Get number of buttons
        num_button = len(labels)
        # Place button based on num
        if num_button == 1:
            # Create button in middle
            first_button = self.create_button(labels[0], (2 if gui else 3, row))
            # Return button
            return [first_button]
        elif num_button == 2:
            # Create button to left and right
            first_button = self.create_button(labels[0], (1, row))
            second_button = self.create_button(labels[1], (3 if gui else 5, row))
            # Return buttons
            return [first_button, second_button]
        else:
            # Create buttons in middle
            first_button = self.create_button(labels[0], (1, row))
            second_button = self.create_button(labels[1], (2 if gui else 3, row))
            third_button = self.create_button(labels[2], (3 if gui else 5, row))
            # Return buttons
            return [first_button, second_button, third_button]

    def create_label(self, text, coord, span=None):
        column, row = coord
        Label(self.win, anchor="center", text=text, font=("Arial", 10, "bold")) \
            .grid(column=column, row=row, columnspan=1 if span is None else span)

    def create_button(self, text, coord):
        button = Button(self.win, text=text)
        widget_grid(button, coord)
        return button

    def create_entry(self, label, string, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        entry = Entry(self.win, textvariable=StringVar(value=string), font=("Arial", 10), width=10)
        widget_grid(entry, coord)
        return label, entry

    def create_checkbutton(self, label, text, boolean, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        bool_var = IntVar(value=boolean)
        checkbutton = Checkbutton(self.win, text=text, variable=bool_var)
        widget_grid(checkbutton, coord)
        return label, bool_var

    def create_option_menu(self, label, options_list, string, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        string_var = StringVar(value=string)
        option_menu = OptionMenu(self.win, string_var, *options_list)
        widget_grid(option_menu, coord)
        return label, string_var

    def create_spinbox(self, label, settings, num, coord, offset=2):
        if label is not None: self.create_label(label, shift_coord(coord, -offset))
        from_, to, increment = settings
        num_var = IntVar(value=num) if isinstance(num, int) else num
        spinbox = Spinbox(self.win, from_=from_, to=to, increment=increment, textvariable=num_var, width=5)
        widget_grid(spinbox, coord)
        return label, spinbox

    def create_scale(self, from_, to, num, coord):
        column, row = coord
        scale = Scale(self.win, from_=from_, to=to, variable=IntVar(value=num),
                      orient=HORIZONTAL, showvalue=False, length=100)
        scale.grid(column=column, row=row, columnspan=2)
        return scale

    def single_spinbox_scale(self, label, settings, initial, coord, offset=3):
        from_, to, factor = settings
        double_var = DoubleVar(value=initial / factor)

        scale = self.create_scale(from_, to, initial, coord)
        scale.configure(command=lambda val: double_var.set(int(val) if factor == 1 else int(val) / factor))

        _, spinbox = self.create_spinbox(label, (from_ / factor, to / factor, 1 / factor),
                                         double_var, shift_coord(coord, 2), offset)
        spinbox.configure(command=lambda: scale.set(double_var.get() * factor))

        return label, spinbox

    def double_spinbox_scale(self, label, coord):

        def inverse_string(string): return 100 - int(string)

        def inverse_num(double): return 1 - double

        self.create_label(label, shift_coord(coord, -1))

        var1 = DoubleVar(value=0.5)
        var2 = DoubleVar(value=0.5)

        _, spinbox1 = self.create_spinbox(None, (0, 1, 0.01), var1, shift_coord(coord, 1))
        spinbox1.configure(command=lambda: [scale.set(var1.get() * 100), var2.set(inverse_num(var1.get()))])

        scale = self.create_scale(0, 100, 50, shift_coord(coord, 2))
        scale.configure(command=lambda val: [var1.set(int(val) / 100), var2.set(inverse_string(val) / 100)])

        _, spinbox2 = self.create_spinbox(None, (0, 1, 0.01), var2, shift_coord(coord, 4))
        spinbox2.configure(
            command=lambda: [scale.set(inverse_num(var2.get()) * 100), var1.set(inverse_num(var2.get()))])

        return label, [spinbox1, spinbox2]

    def triple_spinbox_scale(self, label, first, second, third, coord):
        self.create_label(label, shift_coord(coord, -2))
        _, spinbox1 = self.single_spinbox_scale("Initial", (0, 100, 100), first, shift_coord(coord, 1, -1))
        _, spinbox2 = self.single_spinbox_scale("Final", (0, 100, 100), second, shift_coord(coord, 1))
        _, spinbox3 = self.single_spinbox_scale("Step", (0, 10, 1000), third, shift_coord(coord, 1, 1))
        return label, [spinbox1, spinbox2, spinbox3]

    def vertical_lines(self, first_row, columns, length):
        for col in columns:
            ttk.Separator(self.win, orient=VERTICAL).grid(column=col, row=first_row, rowspan=length, sticky="NS")

    def horizontal_lines(self, row_list, length):
        for row in row_list:
            ttk.Separator(self.win, orient=HORIZONTAL).grid(column=0, row=row, columnspan=length, sticky="EW")

    def place_row_labels(self, row, val_list):
        for index, val in enumerate(val_list):
            self.create_label(val, (2 * index + 1, row))
