from gui.frame_gui import FrameGUI
from .env_simulation import EnvSimulation
from .experiment_results import Results


def convert_dict(widget_list):
    # New dict
    widget_dict = {}
    # Extract widget values
    extract_widget_values(widget_list)

    # Loop through each section
    for (_, section) in widget_list:
        # Loop through each widget
        for label, value in section:
            # Convert to lower case
            label = label.lower()
            # Add underscore
            label = label.replace(" ", "_")
            # Add to dict
            widget_dict[label] = value

    # Return dict
    return widget_dict


def convert_widget_value(value):
    # Value is already int or string
    if isinstance(value, int) or not value.replace(".", "").isnumeric():
        return value
    else:
        return int(value) if value.isnumeric() else float(value)


def extract_widget_values(widget_list):
    # Widget values
    widget_sections = []

    # Loop through each section
    for (_, section) in widget_list:

        # Widget values
        widget_values = []

        # Loop through each widget
        for index, (label, widget) in enumerate(section):

            # Check if widget is list
            if isinstance(widget, list):
                widget_val = [x.get() for x in widget]
                processed_val = [convert_widget_value(x) for x in widget_val]
            else:
                widget_val = widget.get()
                processed_val = convert_widget_value(widget_val)

            # Store processed values
            widget_values.append(processed_val)
            # Combine list to single string
            if isinstance(processed_val, list): processed_val = " / ".join([str(x) for x in processed_val])
            # Replace widget with value
            section[index] = (label, processed_val)

        # Store processed sections
        widget_sections.append(widget_values)

    # Return widget list with values
    return widget_sections


def extract_settings(common_widgets):
    # Unpack widgets list
    [env_widgets, parameter_widgets, other_widgets] = common_widgets

    # Extract settings
    [env_settings, train_settings] = extract_widget_values(env_widgets)
    [parameter_settings, state_space] = extract_widget_values(parameter_widgets)
    other_settings = {} if other_widgets is None else convert_dict(other_widgets)
    parameter_settings.insert(1, tuple(state_space))

    # Return settings
    return env_settings, train_settings, parameter_settings, other_settings


class GymControl:
    def __init__(self):
        # Gym environment
        self.frame_gui = FrameGUI(self.get_results, self.get_hyperparameters)
        self.env_simulation = EnvSimulation()

    def load_gui(self, env_dict, default_env):
        # Load gym frame
        self.frame_gui.load_gym_frame(env_dict, default_env)

    def load_env(self, env_data):
        # Extract settings and functions
        [common_widgets, env_id, env_dict] = env_data
        env_settings, train_settings, parameter_settings, other_settings = extract_settings(common_widgets)

        # Load env functions
        EnvFunctions = env_dict[env_id][1]
        functions = EnvFunctions(parameter_settings, other_settings).env_functions()

        # Load reinforcement learning
        self.env_simulation.unpack_settings(train_settings, functions, other_settings)
        self.env_simulation.create_env(env_id, env_settings)
        self.env_simulation.create_agent(parameter_settings)

        # Return common widgets
        return common_widgets

    def get_results(self, env_data, exp_widgets):
        # Extract exp settings
        [exp_settings] = extract_widget_values(exp_widgets)
        hyperparameters, runs, result_settings = exp_settings[:3], exp_settings[3], exp_settings[4:]
        hyperparameters = [item for sublist in hyperparameters for item in sublist]

        # Run experiment and get results
        common_widgets = self.load_env(env_data)
        results, total_runs = self.env_simulation.run_experiment(hyperparameters, runs, True)
        exp_results = Results(result_settings, results, total_runs).get_statistics()

        # Load results frame
        self.frame_gui.load_results_frame(common_widgets, exp_widgets, exp_results)

    def get_hyperparameters(self, env_data, tune_widgets):
        # Extract tune settings
        [tune_settings] = extract_widget_values(tune_widgets)
        tune_settings = [x[0] if isinstance(x, list) else x for x in tune_settings]

        # Genetic algorithm
        common_widgets = self.load_env(env_data)
        fittest_chromosomes = self.env_simulation.run_genetic_algorithm(tune_settings)

        # Load hyperparameter frame
        self.frame_gui.load_hyperparameter_frame(common_widgets, tune_widgets, fittest_chromosomes)
