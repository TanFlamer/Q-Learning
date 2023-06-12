from gui.env_gui import EnvGUI
from code.reinforcement_learning import ReinforcementLearning
from code.experiment_results import Results


def convert_dict(widget_list):
    # New dict
    widget_dict = {}
    # Loop through each section
    for (_, section) in widget_list:
        # Loop through each widget
        for label, value in section:
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
    # Environment settings
    [env_settings, train_settings] = extract_widget_values(env_widgets)
    # Parameter settings
    [parameter_settings, state_space] = extract_widget_values(parameter_widgets)
    parameter_settings.insert(1, tuple(state_space))
    # Other settings
    other_settings = None if other_widgets is None else convert_dict(other_widgets)
    # Return settings
    return env_settings, train_settings, parameter_settings, other_settings


class GymEnv:
    def __init__(self):
        # Gym environment
        self.env_gui = EnvGUI(self.run_experiment, self.run_genetic_algorithm)
        self.reinforcement_learning = ReinforcementLearning()

    def load_gui(self, env_dict, default_env):
        # Load gym frame
        self.env_gui.load_gym_frame(env_dict, default_env)

    def load_reinforcement_learning(self, env_data):
        # Extract settings and functions
        [common_widgets, env_id, env_dict] = env_data
        env_settings, train_settings, parameter_settings, other_settings = extract_settings(common_widgets)

        # Load env functions
        EnvFunctions = env_dict[env_id][1]
        functions = EnvFunctions(parameter_settings).env_functions()

        # Load reinforcement learning
        self.reinforcement_learning.unpack_settings(train_settings, functions, other_settings)
        self.reinforcement_learning.create_env(env_id, env_settings)
        self.reinforcement_learning.create_agent(parameter_settings)

        # Return common widgets
        return common_widgets

    def run_experiment(self, env_data, exp_widgets):
        # Extract exp settings
        [exp_settings] = extract_widget_values(exp_widgets)
        hyperparameters, runs, result_settings = exp_settings[:3], exp_settings[3], exp_settings[4:]
        hyperparameters = [item for sublist in hyperparameters for item in sublist]

        # Run experiment and get results
        common_widgets = self.load_reinforcement_learning(env_data)
        results, total_runs = self.reinforcement_learning.run_experiment(hyperparameters, runs, True)
        exp_results = Results(result_settings, results, total_runs).get_statistics()

        # Load results frame
        self.env_gui.load_results_frame(common_widgets, exp_widgets, exp_results)

    def run_genetic_algorithm(self, env_data, tune_widgets):
        # Extract tune settings
        [tune_settings] = extract_widget_values(tune_widgets)
        tune_settings = [x[0] if isinstance(x, list) else x for x in tune_settings]

        # Genetic algorithm
        common_widgets = self.load_reinforcement_learning(env_data)
        fittest_chromosomes = self.reinforcement_learning.run_genetic_algorithm(tune_settings)

        # Load hyperparameter frame
        self.env_gui.load_hyperparameter_frame(common_widgets, tune_widgets, fittest_chromosomes)
