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


def shift_coord(coord, column_shift, row_shift=0):
    column, row = coord
    return column + column_shift, row + row_shift
