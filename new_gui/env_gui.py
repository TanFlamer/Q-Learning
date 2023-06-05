# Import the required Libraries
from new_gui.widgets import *


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

    # Environment settings labels
    gym_labels = ["Gym Environment", "Number of Copies", "Render Mode", "Random Seed"]
    place_column_labels(win, gym_labels, 1, range(2, 9, 2))

    # Training settings labels
    training_labels = ["Max Runs", "Max Episodes", "Max Turns"]
    place_column_labels(win, training_labels, 1, range(12, 17, 2))

    # Option lists
    env_list = ["CartPole", "Acrobot"]

    # Environment Settings
    gym_env = create_option_menu(win, StringVar(value="CartPole"), env_list, 3, 2)
    gym_num = create_spinbox(win, 1, 10, 1, IntVar(value=1), 3, 4)
    render_mode = create_checkbutton(win, "Human", IntVar(value=0), 3, 6)
    random_seed = create_entry(win, StringVar(value="20313854"), 3, 8)
    env_settings = [gym_env, gym_num, render_mode, random_seed]

    # Training Settings
    run_num = create_spinbox(win, 1, 10, 1, IntVar(value=1), 3, 12)
    episode_num = create_spinbox(win, 1, 10, 1, IntVar(value=1), 3, 14)
    turn_num = create_spinbox(win, 1, 10, 1, IntVar(value=1), 3, 16)
    training_settings = [run_num, episode_num, turn_num]

    # Button
    parameter_button = create_button(win, "Parameters", 2, 18)
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

    # Parameter settings and State space labels
    parameter_labels = ["Q-Table Number", "Action Space", "Initial Q-Values", "Opposition Learning", "Reward Function"]
    place_column_labels(win, parameter_labels, 1, range(2, 11, 2))
    place_column_labels(win, state_labels, 1, range(14, state_length * 2 + 13, 2))

    # Option lists
    random_types = ["None", "Normal", "Uniform"]
    reward_types = ["Constant-Reward", "Turn-Count", "X-Distance", "X-Distance-Paddle", "XY-Distance"]

    # Parameter Settings
    q_table = create_spinbox(win, 1, 5, 1, IntVar(value=1), 3, 2)
    action = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 4)
    random = create_option_menu(win, StringVar(value="None"), random_types, 3, 6)
    opposition = create_checkbutton(win, "Include", IntVar(value=0), 3, 8)
    reward = create_option_menu(win, StringVar(value="Constant-Reward"), reward_types, 3, 10)
    parameter_settings = [q_table, action, random, opposition, reward]

    # State space
    cart_position = create_spinbox(win, 1, 5, 1, IntVar(value=1), 3, 14)
    cart_velocity = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 16)
    pole_angle = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 18)
    pole_velocity = create_spinbox(win, 2, 3, 1, IntVar(value=2), 3, 20)

    # Buttons
    tuning_button = create_button(win, "Tuning", 1, state_length * 2 + 14)
    back_button = create_button(win, "Back", 2, state_length * 2 + 14)
    experiment_button = create_button(win, "Experiment", 3, state_length * 2 + 14)

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

    # Other setting labels
    game_labels = ["Brick Placement", "Brick Rows", "Brick Columns", "Ball Speed", "Paddle Speed", "Game Mode"]
    place_column_labels(win, game_labels, 1, range(2, 13, 2))

    # Option lists
    brick_types = ["Row", "Column", "Random"]
    factors_list = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]

    # Game Settings
    brick_placement = create_option_menu(win, StringVar(value="Row"), brick_types, 3, 2)
    brick_rows = create_spinbox(win, 1, 6, 1, IntVar(value=3), 3, 4)
    bricks_in_row = create_option_menu(win, IntVar(value=8), factors_list, 3, 6)
    ball_speed = create_spinbox(win, 1, 10, 1, IntVar(value=5), 3, 8)
    paddle_speed = create_spinbox(win, 5, 15, 1, IntVar(value=10), 3, 10)
    game_mode = create_checkbutton(win, "Inverted", IntVar(value=0), 3, 12)
    game_settings = [brick_placement, brick_rows, bricks_in_row, ball_speed, paddle_speed, game_mode]

    # Button
    back_button = create_button(win, "Back", 2, 14)

    # Return widgets
    return win
