# Import the required Libraries
from new_gui.widgets import *
from env_gui import EnvGUI


def get_test_settings(root):
    test_gui = EnvGUI(root)
    # Widget list
    widget_list_1 = [
        ("OptionMenu", ("Gym Environment", ["CartPole", "Acrobot"], "CartPole")),
        ("SpinBox", ("Number of Copies", (1, 10, 1), 1)),
        ("CheckButton", ("Render Mode", "Human", False)),
        ("Entry", ("Random Seed", "20313854"))
    ]
    widget_list_2 = [
        ("SpinBox", ("Max Runs", (1, 10, 1), 1)),
        ("SpinBox", ("Max Episodes", (1, 10, 1), 1)),
        ("SpinBox", ("Max Turns", (1, 10, 1), 1))
    ]
    # Widget lists
    widget_lists = [
        ("Environment Settings", widget_list_1),
        ("Training Settings", widget_list_2)
    ]
    # Button labels
    button_labels = ["Parameters"]
    # Create frame
    return test_gui.create_frame(widget_lists, button_labels)


def get_env_settings(root):
    # Create new frame
    win = Frame(root)

    # Frame dimensions
    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(20): win.grid_rowconfigure(y, weight=1)

    # Title labels
    create_label(win, "Environment Settings", 2, 0)
    create_label(win, "Training Settings", 2, 10)

    # Vertical lines
    place_vertical_lines(win, 1, [0, 2, 4], 9)
    place_vertical_lines(win, 11, [0, 2, 4], 7)

    # Horizontal lines
    place_horizontal_lines(win, range(1, 10, 2), 5)
    place_horizontal_lines(win, range(11, 18, 2), 5)

    # Option lists
    env_list = ["CartPole", "Acrobot"]

    # Environment Settings
    gym_env = create_option_menu(win, "Gym Environment", env_list, "CartPole", (3, 2))
    gym_num = create_spinbox(win, "Number of Copies", (1, 10, 1), 1, (3, 4))
    render_mode = create_checkbutton(win, "Render Mode", "Human", False, (3, 6))
    random_seed = create_entry(win, "Random Seed", "20313854", (3, 8))
    env_settings = [gym_env, gym_num, render_mode, random_seed]

    # Training Settings
    run_num = create_spinbox(win, "Max Runs", (1, 10, 1), 1, (3, 12))
    episode_num = create_spinbox(win, "Max Episodes", (1, 10, 1), 1, (3, 14))
    turn_num = create_spinbox(win, "Max Turns", (1, 10, 1), 1, (3, 16))
    training_settings = [run_num, episode_num, turn_num]

    # Button
    parameter_button = create_button(win, "Parameters", (2, 18))
    return win, parameter_button


def get_parameter_settings(root):
    # Create new frame
    win = Frame(root)

    state_labels = ["Cart Position", "Cart Velocity", "Pole Angle", "Pole Velocity"]
    # state_labels = ["Theta1 Cos", "Theta1 Sin", "Theta2 Cos", "Theta2 Sin", "Theta1 Velocity", "Theta2 Velocity"]
    state_length = len(state_labels)

    # Frame dimensions
    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(16 + state_length * 2): win.grid_rowconfigure(y, weight=1)

    # Title labels
    create_label(win, "Parameter Settings", 2, 0)
    create_label(win, "State Space", 2, 12)

    # Vertical lines
    place_vertical_lines(win, 1, [0, 2, 4], 11)
    place_vertical_lines(win, 13, [0, 2, 4], state_length * 2 + 1)

    # Horizontal lines
    place_horizontal_lines(win, range(1, 12, 2), 5)
    place_horizontal_lines(win, range(13, state_length * 2 + 14, 2), 5)

    # Option lists
    random_types = ["None", "Normal", "Uniform"]
    reward_types = ["Constant-Reward", "Turn-Count", "X-Distance", "X-Distance-Paddle", "XY-Distance"]

    # Parameter Settings
    q_table = create_spinbox(win, "Q-Table Number", (1, 5, 1), 1, (3, 2))
    action = create_spinbox(win, "Action Space", (2, 3, 1), 2, (3, 4))
    random = create_option_menu(win, "Q-Table Initialization", random_types, "None", (3, 6))
    opposition = create_checkbutton(win, "Opposition Learning", "Include", False, (3, 8))
    reward = create_option_menu(win, "Reward Function", reward_types, "Constant-Reward", (3, 10))
    parameter_settings = [q_table, action, random, opposition, reward]

    # State space
    cart_position = create_spinbox(win, "Cart Position", (1, 5, 1), 1, (3, 14))
    cart_velocity = create_spinbox(win, "Cart Velocity", (2, 3, 1), 2, (3, 16))
    pole_angle = create_spinbox(win, "Pole Angle", (2, 3, 1), 2, (3, 18))
    pole_velocity = create_spinbox(win, "Pole Velocity", (2, 3, 1), 2, (3, 20))

    # Buttons
    tuning_button = create_button(win, "Tuning", (1, state_length * 2 + 14))
    back_button = create_button(win, "Back", (2, state_length * 2 + 14))
    experiment_button = create_button(win, "Experiment", (3, state_length * 2 + 14))

    return win


def get_game_settings(root):
    # Create new frame
    win = Frame(root)

    # Frame dimensions
    for x in range(5): win.grid_columnconfigure(x, weight=1)
    for y in range(16): win.grid_rowconfigure(y, weight=1)

    # Title label
    create_label(win, "Game Settings", 2, 0)

    # Vertical line
    place_vertical_lines(win, 1, [0, 2, 4], 13)

    # Horizontal line
    place_horizontal_lines(win, range(1, 14, 2), 5)

    # Option lists
    brick_types = ["Row", "Column", "Random"]
    factors_list = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]

    # Game Settings
    brick_placement = create_option_menu(win, "Brick Placement", brick_types, "Row", (3, 2))
    brick_rows = create_spinbox(win, "Brick Rows", (1, 6, 1), 3, (3, 4))
    bricks_in_row = create_option_menu(win, "Brick Columns", factors_list, "8", (3, 6))
    ball_speed = create_spinbox(win, "Ball Speed", (1, 10, 1), 5, (3, 8))
    paddle_speed = create_spinbox(win, "Paddle Speed", (5, 15, 1), 10, (3, 10))
    game_mode = create_checkbutton(win, "Game Mode", "Inverted", False, (3, 12))
    game_settings = [brick_placement, brick_rows, bricks_in_row, ball_speed, paddle_speed, game_mode]

    # Button
    back_button = create_button(win, "Back", (2, 14))

    # Return widgets
    return win
