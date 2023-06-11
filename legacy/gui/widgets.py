# Import the required Libraries
from tkinter import *
from tkinter import ttk


def get_widget_values(var_list):
    values = [var.get() for var in var_list]
    return [process_widget_value(value) for value in values]


def process_widget_value(value):
    # Value is already int or string
    if isinstance(value, int) or not value.replace(".", "").isnumeric():
        return value
    else:
        return int(value) if value.isnumeric() else float(value)


def get_col_index(index):
    remainder = index % 3
    return 2 * remainder + 1


def get_row_index(index, offset):
    factor = index // 3
    row_num = 3 * factor + offset
    return [row_num, row_num + 1]


def combine_chromosome_genes(hyper_parameters):
    parameter_lists = [hyper_parameters[:3], hyper_parameters[3:6], hyper_parameters[6:]]
    return [" / ".join([str(x) for x in parameter_list]) for parameter_list in parameter_lists]


def get_inverse_value(val_list):
    return [str(val) + " / " + str(1 - val) for val in val_list]


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


def create_entry(root, string_var, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    entry = Entry(root, textvariable=string_var, font=("Arial", 10), width=10)
    entry.grid(column=column, row=row)
    return entry


def create_button(root, text, column, row):
    button = Button(root, text=text)
    button.grid(column=column, row=row)
    return button


def create_checkbutton(root, text, int_var, column, row):
    checkbutton = Checkbutton(root, text=text, variable=int_var)
    checkbutton.grid(column=column, row=row)
    return int_var


def create_option_menu(root, var, options_list, column, row):
    option_menu = OptionMenu(root, var, *options_list)
    option_menu.grid(column=column, row=row)
    return var


def create_spinbox(root, from_, to, increment, num_var, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    spinbox = Spinbox(root, from_=from_, to=to, increment=increment, textvariable=num_var, width=5)
    spinbox.grid(column=column, row=row)
    return spinbox


def create_scale(root, from_, to, int_var, column, row):
    scale = Scale(root, from_=from_, to=to, variable=int_var, orient=HORIZONTAL, showvalue=False, length=100)
    scale.grid(column=column, row=row, columnspan=2)
    return scale


def single_spinbox_scale(root, from_, to, initial, factor, column, row, text=None):
    if text is not None: create_label(root, text, column - 1, row)
    double_var = DoubleVar(value=initial / factor)

    scale = create_scale(root, from_, to, IntVar(value=initial), column, row)
    scale.configure(command=lambda val: double_var.set(int(val) if factor == 1 else int(val) / factor))

    spinbox = create_spinbox(root, from_ / factor, to / factor, 1 / factor, double_var, column + 2, row)
    spinbox.configure(command=lambda: scale.set(double_var.get() * factor))

    return spinbox


def double_spinbox_scale(root, column, row):
    def inverse_string(string): return 100 - int(string)

    def inverse_num(double): return 1 - double

    var1 = DoubleVar(value=0.5)
    var2 = DoubleVar(value=0.5)

    spinbox1 = create_spinbox(root, 0, 1, 0.01, var1, column + 1, row)
    spinbox1.configure(command=lambda: [scale.set(var1.get() * 100), var2.set(inverse_num(var1.get()))])

    scale = create_scale(root, 0, 100, IntVar(value=50), column + 2, row)
    scale.configure(command=lambda val: [var1.set(int(val) / 100), var2.set(inverse_string(val) / 100)])

    spinbox2 = create_spinbox(root, 0, 1, 0.01, var2, column + 4, row)
    spinbox2.configure(command=lambda: [scale.set(inverse_num(var2.get()) * 100), var1.set(inverse_num(var2.get()))])

    return spinbox1


def triple_spinbox_scale(root, first, second, third, column, row):
    labels = ["Initial", "Final", "Step"]
    rows = [row - 1, row, row + 1]
    place_column_labels(root, labels, column, rows)

    spinbox1 = single_spinbox_scale(root, 0, 100, first, 100, column + 1, row - 1)
    spinbox2 = single_spinbox_scale(root, 0, 100, second, 100, column + 1, row)
    spinbox3 = single_spinbox_scale(root, 0, 10, third, 1000, column + 1, row + 1)

    return [spinbox1, spinbox2, spinbox3]
