from tkinter import *
from tkinter import ttk


def shift_coord(coord, column_shift, row_shift=0):
    column, row = coord
    return column + column_shift, row + row_shift


def widget_grid(widget, coord):
    column, row = coord
    widget.grid(column=column, row=row)


def link_button(button, first_frame, second_frame, open_frame=True):
    # Link button to command
    if open_frame:
        # Keep frame open
        button.configure(command=lambda: [first_frame.pack_forget(), second_frame.pack(fill='both', expand=1)])
    else:
        # Close frame for experiment
        button.configure(command=lambda: [first_frame.destroy()])


class EnvGUI:
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

    def create_frame(self, widget_lists, button_labels):
        # Row count
        rows = 0
        # Create sections
        for x in range(len(widget_lists)):
            # Unpack section widgets
            label, widget_list = widget_lists[x]
            # Create sections
            self.create_section(label, widget_list, rows)
            # Number of widgets in section
            num_widget = len(widget_list)
            # Add to total
            rows += (num_widget + 1) * 2
        # Add buttons
        button_list = self.add_buttons(button_labels, rows)
        # Configure grid rows and columns
        for x in range(5): self.win.grid_columnconfigure(x, weight=1)
        for y in range(rows + 2): self.win.grid_rowconfigure(y, weight=1)
        # Return frame and button list
        return self.win, button_list

    def create_section(self, label, widget_list, row):
        # Number of widgets
        num_widget = len(widget_list)
        # Section label
        self.create_label(label, (2, row))
        # Section lines
        self.vertical_lines(row + 1, [0, 2, 4], num_widget * 2 + 1)
        self.horizontal_lines(range(row + 1, row + (num_widget + 1) * 2, 2), 5)
        # Place widgets
        widget_values = []
        for index in range(num_widget):
            widget_type, widget_settings = widget_list[index]
            widget_value = self.widgets[widget_type](*widget_settings, (3, row + (index + 1) * 2))
            widget_values.append(widget_value)
        # Return widget list
        return widget_values

    def add_buttons(self, labels, row):
        # Get number of buttons
        num_button = len(labels)
        # Place button based on num
        if num_button == 1:
            # Create button in middle
            first_button = self.create_button(labels[0], (2, row))
            # Return button
            return [first_button]
        elif num_button == 2:
            # Create button to left and right
            first_button = self.create_button(labels[0], (1, row))
            second_button = self.create_button(labels[0], (3, row))
            # Return buttons
            return [first_button, second_button]
        else:
            # Create buttons in middle
            first_button = self.create_button(labels[0], (1, row))
            second_button = self.create_button(labels[0], (2, row))
            third_button = self.create_button(labels[0], (3, row))
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
        return entry

    def create_checkbutton(self, label, text, boolean, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        bool_var = IntVar(value=boolean)
        checkbutton = Checkbutton(self.win, text=text, variable=bool_var)
        widget_grid(checkbutton, coord)
        return bool_var

    def create_option_menu(self, label, options_list, string, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        string_var = StringVar(value=string)
        option_menu = OptionMenu(self.win, string_var, *options_list)
        widget_grid(option_menu, coord)
        return string_var

    def create_spinbox(self, label, settings, num, coord, offset=2):
        self.create_label(label, shift_coord(coord, -offset))
        from_, to, increment = settings
        num_var = IntVar(value=num) if isinstance(num, int) else num
        spinbox = Spinbox(self.win, from_=from_, to=to, increment=increment, textvariable=num_var, width=5)
        widget_grid(spinbox, coord)
        return spinbox

    def create_scale(self, from_, to, num, coord):
        column, row = coord
        scale = Scale(self.win, from_=from_, to=to, variable=IntVar(value=num),
                      orient=HORIZONTAL, showvalue=False, length=100)
        scale.grid(column=column, row=row, columnspan=2)
        return scale

    def single_spinbox_scale(self, label, settings, initial, coord):
        from_, to, factor = settings
        double_var = DoubleVar(value=initial / factor)

        scale = self.create_scale(from_, to, initial, coord)
        scale.configure(command=lambda val: double_var.set(int(val) if factor == 1 else int(val) / factor))

        spinbox = self.create_spinbox(label, (from_/factor, to/factor, 1/factor), double_var, shift_coord(coord, 2))
        spinbox.configure(command=lambda: scale.set(double_var.get() * factor))

        return spinbox

    def double_spinbox_scale(self, label, coord):

        def inverse_string(string): return 100 - int(string)
        def inverse_num(double): return 1 - double

        self.create_label(label, shift_coord(coord, -1))

        var1 = DoubleVar(value=0.5)
        var2 = DoubleVar(value=0.5)

        spinbox1 = self.create_spinbox("", (0, 1, 0.01), var1, shift_coord(coord, 1))
        spinbox1.configure(command=lambda: [scale.set(var1.get() * 100), var2.set(inverse_num(var1.get()))])

        scale = self.create_scale(0, 100, 50, shift_coord(coord, 2))
        scale.configure(command=lambda val: [var1.set(int(val) / 100), var2.set(inverse_string(val) / 100)])

        spinbox2 = self.create_spinbox("", (0, 1, 0.01), var2, shift_coord(coord, 4))
        spinbox2.configure(command=lambda: [scale.set(inverse_num(var2.get()) * 100),var1.set(inverse_num(var2.get()))])

        return spinbox1

    def triple_spinbox_scale(self, first, second, third, coord):
        spinbox1 = self.single_spinbox_scale("Initial", (0, 100, 100), first, shift_coord(coord, 1, -1))
        spinbox2 = self.single_spinbox_scale("Final", (0, 100, 100), second, shift_coord(coord, 1))
        spinbox3 = self.single_spinbox_scale("Step", (0, 10, 1000), third, shift_coord(coord, 1, 1))
        return [spinbox1, spinbox2, spinbox3]

    def vertical_lines(self, first_row, columns, length):
        for col in columns:
            ttk.Separator(self.win, orient=VERTICAL).grid(column=col, row=first_row, rowspan=length, sticky="NS")

    def horizontal_lines(self, row_list, length):
        for row in row_list:
            ttk.Separator(self.win, orient=HORIZONTAL).grid(column=0, row=row, columnspan=length, sticky="EW")

    def place_row_labels(self, row, val_list):
        for index, val in enumerate(val_list):
            self.create_label(val, 2 * index + 1, row)
