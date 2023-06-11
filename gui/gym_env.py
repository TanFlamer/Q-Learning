from gui.env_gui import EnvGUI
from code.reinforcement_learning import ReinforcementLearning
from code.experiment_results import Results


def link_frame(button, first_frame, second_frame):
    # Link button to change frame
    button.configure(command=lambda: [first_frame.pack_forget(), second_frame.pack(fill='both', expand=1)])


def link_function(button, frame, function, variables):
    # Link button to function
    button.configure(command=lambda: [frame.pack_forget(), frame.master.withdraw(), function(*variables)])


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
    def __init__(self, env_dict, default_env):
        # Gym environment
        self.env_gui = EnvGUI()
        self.env_dict = env_dict
        self.default_env = default_env
        self.gym_frame = None
        self.env_id = None

    def load_gym_frame(self):
        # Get env list
        env_list = list(self.env_dict.keys())
        # Create gym frame
        self.gym_frame, [(_, [(_, gym_env)])], [next_button] = self.env_gui.get_gym_frame(env_list, self.default_env)
        # Configure back button
        next_button.configure(command=lambda: self.load_all_frames(gym_env.get()))
        # Pack gym frame
        self.gym_frame.pack(fill='both', expand=1)
        # Load main loop
        self.env_gui.main.mainloop()

    def load_all_frames(self, env_id):
        # Save env id
        self.env_id = env_id

        # Load env settings
        EnvSettings = self.env_dict[self.env_id][0]
        settings = EnvSettings().env_settings()

        # Load env frame
        env_frame, env_widgets, [other_button, gym_button, parameter_button] = self.load_env_frame(settings)
        # Load parameter frame
        parameter_frame, parameter_widgets, [tune_button, env_button, exp_button] = self.load_parameter_frame(settings)
        # Load other frame
        other_frame, other_widgets, other_buttons = self.load_other_frame(settings)
        # Load experiment frame
        exp_frame, exp_widgets, [exp_back_button, exp_start_button] = self.load_experiment_frame(settings)
        # Load hyperparameter frame
        tune_frame, tune_widgets, [tune_back_button, tune_start_button] = self.load_tune_frame()

        # Link button to frames
        link_frame(gym_button, env_frame, self.gym_frame)
        link_frame(parameter_button, env_frame, parameter_frame)
        link_frame(env_button, parameter_frame, env_frame)
        link_frame(tune_button, parameter_frame, tune_frame)
        link_frame(exp_button, parameter_frame, exp_frame)
        link_frame(exp_back_button, exp_frame, parameter_frame)
        link_frame(tune_back_button, tune_frame, parameter_frame)

        # Check if other settings exist
        if other_frame is not None:
            # From env to other frame
            link_frame(other_button, env_frame, other_frame)
            # From other to env frame
            link_frame(other_buttons[0], other_frame, env_frame)

        # Link button to functions
        common_widgets = [env_widgets, parameter_widgets, other_widgets]
        link_function(exp_start_button, exp_frame, self.run_experiment, (common_widgets, exp_widgets))
        link_function(tune_start_button, tune_frame, self.run_genetic_algorithm, (common_widgets, tune_widgets))

        # Change frame
        self.gym_frame.pack_forget()
        env_frame.pack(fill='both', expand=1)

    def load_settings_frames(self, common_widgets):
        # Unpack widgets list
        [env_widgets, parameter_widgets, other_widgets] = common_widgets
        # Load settings frame
        settings_frame, [other_button, results_button] = self.load_settings_frame(env_widgets + parameter_widgets)
        # Load other frame
        other_frame, other_buttons = self.load_extra_frame(other_widgets)

        # Check if other settings exist
        if other_frame is not None:
            # From settings to other
            link_frame(other_button, settings_frame, other_frame)
            # From other to settings
            link_frame(other_buttons[0], other_frame, settings_frame)

        # Return settings frame
        return settings_frame, results_button

    def run_experiment(self, common_widgets, exp_widgets):
        # Reinforcement learning
        reinforcement_learning, other_settings = self.load_reinforcement_learning(common_widgets)

        # Extract exp settings
        [exp_settings] = extract_widget_values(exp_widgets)
        hyperparameters, runs, result_settings = exp_settings[:3], exp_settings[3], exp_settings[4:]
        hyperparameters = [item for sublist in hyperparameters for item in sublist]

        # Run experiment and get results
        results, total_runs = reinforcement_learning.run_experiment(hyperparameters, other_settings, runs, True)
        exp_results = Results(result_settings, results, total_runs)
        results = exp_results.get_statistics()

        # Load settings frame
        settings_frame, results_button = self.load_settings_frames(common_widgets)
        # Load results frame
        results_frame, [back_button, done_button] = self.load_results_frame(exp_widgets, results)

        # Link frames to buttons
        link_frame(results_button, settings_frame, results_frame)
        link_frame(back_button, results_frame, settings_frame)
        done_button.configure(command=lambda: results_frame.master.destroy())

        # Load frame
        settings_frame.master.deiconify()
        settings_frame.pack(fill='both', expand=1)

    def run_genetic_algorithm(self, common_widgets, tune_widgets):
        # Reinforcement learning
        reinforcement_learning, other_settings = self.load_reinforcement_learning(common_widgets)

        # Extract tune settings
        [tune_settings] = extract_widget_values(tune_widgets)
        tune_settings = [x[0] if isinstance(x, list) else x for x in tune_settings]

        # Genetic algorithm
        fittest_chromosomes = reinforcement_learning.run_genetic_algorithm(tune_settings, other_settings)

        # Load settings frame
        settings_frame, results_button = self.load_settings_frames(common_widgets)
        # Load hyperparameter frame
        hyperparameter_frame, [back_button, done_button] = self.load_hyperparameter_frame(tune_widgets,
                                                                                          fittest_chromosomes)

        # Link frames to buttons
        link_frame(results_button, settings_frame, hyperparameter_frame)
        link_frame(back_button, hyperparameter_frame, settings_frame)
        done_button.configure(command=lambda: hyperparameter_frame.master.destroy())

        # Load frame
        settings_frame.master.deiconify()
        settings_frame.pack(fill='both', expand=1)

    def load_reinforcement_learning(self, common_widgets):
        # Extract settings and functions
        env_settings, train_settings, parameter_settings, other_settings = extract_settings(common_widgets)

        # Load env functions
        EnvFunctions = self.env_dict[self.env_id][1]
        functions = EnvFunctions(parameter_settings).env_functions()

        # Load reinforcement learning
        reinforcement_learning = ReinforcementLearning(train_settings, functions)
        reinforcement_learning.create_env(self.env_id, env_settings)
        reinforcement_learning.create_agent(parameter_settings)

        # Return reinforcement learning
        return reinforcement_learning, other_settings

    def load_env_frame(self, settings):
        # Load run settings
        run_settings = settings["Run"]
        # Create env frame
        return self.env_gui.get_env_frame(run_settings)

    def load_parameter_frame(self, settings):
        # Load parameter settings
        parameter_settings = settings["Parameter"]
        # Load state spaces
        state_space = settings["State"]
        # Create parameter frame
        return self.env_gui.get_parameter_frame(parameter_settings, state_space)

    def load_other_frame(self, settings):
        # Load other settings
        other_settings = settings["Other"]
        # Create other frame
        return self.env_gui.get_other_frame(other_settings)

    def load_experiment_frame(self, settings):
        # Load original results
        original_results = settings["Results"]
        # Create experiment frame
        return self.env_gui.get_experiment_frame(original_results)

    def load_tune_frame(self):
        # Create hyperparameter frame
        return self.env_gui.get_tune_frame()

    def load_settings_frame(self, main_settings):
        # Create settings frame
        return self.env_gui.get_settings_frame(main_settings)

    def load_results_frame(self, exp_settings, results):
        # Create results frame
        return self.env_gui.get_results_frame(exp_settings, results)

    def load_hyperparameter_frame(self, tune_settings, fittest_chromosomes):
        # Create hyperparameter frame
        return self.env_gui.get_hyperparameter_frame(tune_settings, fittest_chromosomes)

    def load_extra_frame(self, other_settings):
        # Create other frame
        return self.env_gui.get_extra_frame(other_settings)
