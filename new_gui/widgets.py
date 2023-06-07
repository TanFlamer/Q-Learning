# Import the required Libraries
from tkinter import *
from tkinter import ttk
from support_functions import *


def place_vertical_lines(root, first_row, columns, length):
    for col in columns:
        ttk.Separator(root, orient=VERTICAL).grid(column=col, row=first_row, rowspan=length, sticky="NS")


def place_horizontal_lines(root, row_list, length):
    for row in row_list:
        ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=row, columnspan=length, sticky="EW")


def place_row_labels(root, row, val_list):
    for index, val in enumerate(val_list):
        create_label(root, val, 2 * index + 1, row)


def place_column_labels(root, text_list, column, row_list):
    for (text, row) in zip(text_list, row_list):
        create_label(root, text, column, row)


def create_label(root, text, column, row, span=None):
    Label(root, anchor="center", text=text, font=("Arial", 10, "bold")) \
        .grid(column=column, row=row, columnspan=1 if span is None else span)


def create_entry(root, label, string, coord, offset=2):
    column, row = coord
    create_label(root, label, column - offset, row)
    entry = Entry(root, textvariable=StringVar(value=string), font=("Arial", 10), width=10)
    entry.grid(column=column, row=row)
    return entry


def create_button(root, text, coord):
    column, row = coord
    button = Button(root, text=text)
    button.grid(column=column, row=row)
    return button


def create_checkbutton(root, label, text, boolean, coord, offset=2):
    column, row = coord
    create_label(root, label, column - offset, row)
    bool_var = IntVar(value=boolean)
    checkbutton = Checkbutton(root, text=text, variable=bool_var)
    checkbutton.grid(column=column, row=row)
    return bool_var


def create_option_menu(root, label, options_list, string, coord, offset=2):
    column, row = coord
    create_label(root, label, column - offset, row)
    string_var = StringVar(value=string)
    option_menu = OptionMenu(root, string_var, *options_list)
    option_menu.grid(column=column, row=row)
    return string_var


def create_spinbox(root, label, settings, num, coord, offset=2):
    column, row = coord
    create_label(root, label, column - offset, row)
    from_, to, increment = settings
    num_var = IntVar(value=num) if isinstance(num, int) else num
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=num_var, width=5)
    spinbox.grid(column=column, row=row)
    return spinbox


def create_scale(root, label, settings, num, coord, offset=2):
    column, row = coord
    create_label(root, label, column - offset, row)
    from_, to, show = settings
    scale = Scale(root, from_=from_, to=to, variable=IntVar(value=num), orient=HORIZONTAL, showvalue=show, length=100)
    scale.grid(column=column, row=row, columnspan=2)
    return scale


def single_spinbox_scale(root, label, settings, initial, coord):
    from_, to, factor = settings
    double_var = DoubleVar(value=initial / factor)

    scale = create_scale(root, "", (from_, to, False), IntVar(value=initial), coord)
    scale.configure(command=lambda val: double_var.set(int(val) if factor == 1 else int(val) / factor))

    spinbox = create_spinbox(root, label, (from_ / factor, to / factor, 1 / factor), double_var, shift_coord(coord, 2))
    spinbox.configure(command=lambda: scale.set(double_var.get() * factor))

    return spinbox


def double_spinbox_scale(root, label, coord):

    def inverse_string(string): return 100 - int(string)
    def inverse_num(double): return 1 - double

    var1 = DoubleVar(value=0.5)
    var2 = DoubleVar(value=0.5)

    spinbox1 = create_spinbox(root, "", (0, 1, 0.01), var1, shift_coord(coord, 1))
    spinbox1.configure(command=lambda: [scale.set(var1.get() * 100), var2.set(inverse_num(var1.get()))])

    scale = create_scale(root, label, (0, 100, False), IntVar(value=50), shift_coord(coord, 2))
    scale.configure(command=lambda val: [var1.set(int(val) / 100), var2.set(inverse_string(val) / 100)])

    spinbox2 = create_spinbox(root, "", (0, 1, 0.01), var2, shift_coord(coord, 4))
    spinbox2.configure(command=lambda: [scale.set(inverse_num(var2.get()) * 100), var1.set(inverse_num(var2.get()))])

    return spinbox1


def triple_spinbox_scale(root, first, second, third, coord):
    spinbox1 = single_spinbox_scale(root, "Initial", (0, 100, 100), first, shift_coord(coord, 1, -1))
    spinbox2 = single_spinbox_scale(root, "Final", (0, 100, 100), second, shift_coord(coord, 1))
    spinbox3 = single_spinbox_scale(root, "Step", (0, 10, 1000), third, shift_coord(coord, 1, 1))
    return [spinbox1, spinbox2, spinbox3]
