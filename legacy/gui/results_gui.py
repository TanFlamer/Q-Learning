# Import the required Libraries
from .widgets import *


def display_init_settings(root, init_settings):
    # Create new frame
    win = Frame(root)

    # Frame dimensions
    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(22): win.grid_rowconfigure(y, weight=1)

    # Title labels
    create_label(win, "Game Settings", 3, 0)
    create_label(win, "Parameter Settings", 3, 11)

    # Vertical lines
    place_vertical_lines(win, 1, range(0, 7, 2), 10)
    place_vertical_lines(win, 12, range(0, 7, 2), 7)

    # Horizontal lines
    place_horizontal_lines(win, range(1, 11, 3), 7)
    place_horizontal_lines(win, range(12, 19, 3), 7)

    # Split initial settings
    game_settings, parameter_settings = init_settings[:8], init_settings[8:]

    # Game settings labels
    game_labels = ["Random Seed", "Brick Placement", "Brick Rows", "Brick Columns",
                   "Ball Speed", "Paddle Speed", "Game Mode", "Max Episodes"]
    game_data = zip(game_labels, game_settings)

    # Display game settings data
    for index, data in enumerate(game_data):
        place_column_labels(win, list(data), get_col_index(index), get_row_index(index, 2))

    # Parameter settings labels
    parameter_labels = ["Q-Table Number", "State Space", "Action Space",
                        "Q-Table Initialization", "Opposition Learning", "Reward Function"]
    parameter_data = zip(parameter_labels, parameter_settings)

    # Display parameter settings data
    for index, data in enumerate(parameter_data):
        place_column_labels(win, list(data), get_col_index(index), get_row_index(index, 13))

    # Next button
    next_button = create_button(win, "Next", 3, 19)

    # Return button
    return win, next_button


def display_exp_settings(root, exp_settings, results):
    # Create new frame
    win = Frame(root)

    # Frame dimensions
    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(24): win.grid_rowconfigure(y, weight=1)

    # Title labels
    create_label(win, "Experiment Settings", 3, 0)
    create_label(win, "Results", 3, 11)

    # Vertical lines
    place_vertical_lines(win, 1, range(0, 7, 2), 10)
    place_vertical_lines(win, 12, range(0, 7, 2), 10)

    # Horizontal lines
    place_horizontal_lines(win, range(1, 11, 3), 7)
    place_horizontal_lines(win, range(12, 22, 3), 7)

    # Experiment settings labels
    exp_labels = ["Learning Rate", "Explore Rate", "Discount Factor",
                  "New Runs", "Confidence", "Old Mean", "Old STD", "Old Runs"]
    exp_settings = combine_chromosome_genes(exp_settings[:9]) + exp_settings[9:]
    exp_data = zip(exp_labels, exp_settings)

    # Display experiment settings data
    for index, data in enumerate(exp_data):
        place_column_labels(win, list(data), get_col_index(index), get_row_index(index, 2))

    # Results labels
    results_label = ["Mean", "STD", "Median", "IQR", "Max", "Min", "Difference", "Failed"]
    results_data = zip(results_label, results)

    # Display results data
    for index, data in enumerate(results_data):
        place_column_labels(win, list(data), get_col_index(index), get_row_index(index, 13))

    # Buttons
    back_button = create_button(win, "Back", 1, 22)
    done_button = create_button(win, "Done", 5, 22)

    # Return buttons
    return win, back_button, done_button


def display_tune_settings(root, tune_settings, best_chromosomes):
    # Create new frame
    win = Frame(root)

    # Get chromosome list length
    length = len(best_chromosomes)

    # Frame dimensions
    for x in range(7): win.grid_columnconfigure(x, weight=1)
    for y in range(length + 18): win.grid_rowconfigure(y, weight=1)

    # Title labels
    create_label(win, "Tuning Settings", 3, 0)
    create_label(win, "Hyper-parameters", 3, 11)

    # Vertical lines
    place_vertical_lines(win, 1, range(0, 7, 2), 10)
    place_vertical_lines(win, 12, range(0, 7, 2), length + 4)

    # Horizontal lines
    place_horizontal_lines(win, range(1, 11, 3), 7)
    place_horizontal_lines(win, [12, 14, length + 15], 7)

    # Tuning settings labels
    tune_labels = ["Crossover Rate", "Mutation Rate", "Single / Double", "Tournament / Roulette",
                   "Population", "Elite", "Generation", "Best"]
    tune_settings[2:4] = get_inverse_value(tune_settings[2:4])
    tune_data = zip(tune_labels, tune_settings)

    # Display tuning settings data
    for index, data in enumerate(tune_data):
        place_column_labels(win, list(data), get_col_index(index), get_row_index(index, 2))

    # Chromosome labels
    hyper_parameters = ["Learning Rate", "Explore Rate", "Discount Factor"]
    place_row_labels(win, 13, hyper_parameters)

    # Display chromosome data
    joined_chromosomes = [combine_chromosome_genes(chromosome) for chromosome in best_chromosomes]
    for index, chromosome in enumerate(joined_chromosomes):
        place_row_labels(win, index + 15, chromosome)

    # Buttons
    back_button = create_button(win, "Back", 1, length + 16)
    done_button = create_button(win, "Done", 5, length + 16)

    # Return buttons
    return win, back_button, done_button


def display_exp_results(root, init_settings, exp_settings, results):
    # Load frames
    init_frame, next_button = display_init_settings(root, init_settings)
    exp_frame, back_button, done_button = display_exp_settings(root, exp_settings, results)

    # Load buttons
    next_button.configure(command=lambda: [exp_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    back_button.configure(command=lambda: [init_frame.pack(fill='both', expand=1), exp_frame.pack_forget()])
    done_button.configure(command=lambda: root.destroy())

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    root.mainloop()


def display_tune_results(root, init_settings, tune_settings, best_chromosomes):
    # Load frames
    init_frame, next_button = display_init_settings(root, init_settings)
    tune_frame, back_button, done_button = display_tune_settings(root, tune_settings, best_chromosomes)

    # Load buttons
    next_button.configure(command=lambda: [tune_frame.pack(fill='both', expand=1), init_frame.pack_forget()])
    back_button.configure(command=lambda: [init_frame.pack(fill='both', expand=1), tune_frame.pack_forget()])
    done_button.configure(command=lambda: root.destroy())

    # Load frame and run
    init_frame.pack(fill='both', expand=1)
    root.mainloop()
