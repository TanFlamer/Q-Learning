# Import the required Libraries
from tkinter import Tk
from .frame_widgets import FrameWidgets


def link_frame(button, first_frame, second_frame):
    # Link button to change frame
    button.configure(command=lambda: [first_frame.pack_forget(), second_frame.pack(fill='both', expand=1)])


def link_function(button, frame, function, variables):
    # Link button to function
    button.configure(command=lambda: [frame.pack_forget(), frame.master.withdraw(), function(*variables)])


class EnvGUI:
    def __init__(self, exp_func, tune_func):
        # Create main window
        self.main = Tk()
        self.main.title("Brick Breaker")
        self.main.geometry("600x450")
        # Env functions
        self.exp_func = exp_func
        self.tune_func = tune_func

    def load_gym_frame(self, env_dict, default_env):
        # Create gym frame
        gym_frame, [(_, [(_, gym_env)])], [next_button] = self.get_gym_frame(env_dict, default_env)
        # Configure back button
        next_button.configure(command=lambda: self.load_initial_frames(gym_env.get(), env_dict, gym_frame))
        # Pack gym frame
        gym_frame.pack(fill='both', expand=1)
        # Load main loop
        self.main.mainloop()

    def load_initial_frames(self, env_id, env_dict, gym_frame):
        # Load env settings
        EnvSettings = env_dict[env_id][0]
        settings = EnvSettings().env_settings()

        # Load env frame
        env_frame, env_widgets, [other_button, gym_button, parameter_button] = self.get_env_frame(settings)
        # Load parameter frame
        parameter_frame, parameter_widgets, [tune_button, env_button, exp_button] = self.get_parameter_frame(settings)
        # Load other frame
        other_frame, other_widgets, other_buttons = self.get_other_frame(settings)
        # Load experiment frame
        exp_frame, exp_widgets, [exp_back_button, exp_start_button] = self.get_experiment_frame(settings)
        # Load hyperparameter frame
        tune_frame, tune_widgets, [tune_back_button, tune_start_button] = self.get_tune_frame()

        # Link button to frames
        link_frame(gym_button, env_frame, gym_frame)
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
        env_data = [common_widgets, env_id, env_dict]
        link_function(exp_start_button, exp_frame, self.exp_func, (env_data, exp_widgets))
        link_function(tune_start_button, tune_frame, self.tune_func, (env_data, tune_widgets))

        # Change frame
        gym_frame.pack_forget()
        env_frame.pack(fill='both', expand=1)

    def load_final_frames(self, common_widgets):
        # Unpack widgets list
        [env_widgets, parameter_widgets, other_widgets] = common_widgets
        # Load settings frame
        settings_frame, [other_button, results_button] = self.get_settings_frame(env_widgets + parameter_widgets)
        # Load other frame
        other_frame, other_buttons = self.get_extra_frame(other_widgets)

        # Check if other settings exist
        if other_frame is not None:
            # From settings to other
            link_frame(other_button, settings_frame, other_frame)
            # From other to settings
            link_frame(other_buttons[0], other_frame, settings_frame)

        # Return settings frame
        return settings_frame, results_button

    def load_results_frame(self, common_widgets, exp_widgets, exp_results):
        # Load settings frame
        settings_frame, results_button = self.load_final_frames(common_widgets)
        # Load results frame
        results_frame, [back_button, done_button] = self.get_results_frame(exp_widgets, exp_results)

        # Link frames to buttons
        link_frame(results_button, settings_frame, results_frame)
        link_frame(back_button, results_frame, settings_frame)
        done_button.configure(command=lambda: self.main.destroy())

        # Change frame
        settings_frame.master.deiconify()
        settings_frame.pack(fill='both', expand=1)

    def load_hyperparameter_frame(self, common_widgets, tune_widgets, fittest_chromosomes):
        # Load settings frame
        settings_frame, results_button = self.load_final_frames(common_widgets)
        # Load hyperparameter frame
        hyperparameter_frame, [back_button, done_button] = self.get_hyperparameter_frame(tune_widgets, fittest_chromosomes)

        # Link frames to buttons
        link_frame(results_button, settings_frame, hyperparameter_frame)
        link_frame(back_button, hyperparameter_frame, settings_frame)
        done_button.configure(command=lambda: self.main.destroy())

        # Change frame
        settings_frame.master.deiconify()
        settings_frame.pack(fill='both', expand=1)

    def get_gym_frame(self, env_dict, default_env):
        # Create gym subframe
        gym_frame = FrameWidgets(self.main)
        # Get env list
        env_list = list(env_dict.keys())
        # Get gym settings
        gym_settings = [
            ("OptionMenu", ("Gym Environment", env_list, default_env))
        ]
        # Widget lists
        widget_lists = [
            ("Gym Settings", gym_settings)
        ]
        # Button labels
        button_labels = ["Next"]
        # Return frame, widgets and buttons
        return gym_frame.create_gui_frame(widget_lists, button_labels)

    def get_env_frame(self, settings):
        # Create initial subframe
        env_frame = FrameWidgets(self.main)
        # Load run settings
        run_settings = settings["Run"]
        # Get environment settings
        environment_settings = [
            ("SpinBox", ("Number of Copies", (1, 10, 1), 1)),
            ("CheckButton", ("Render Mode", "Human", False)),
            ("Entry", ("Random Seed", "20313854"))
        ]
        # Get training settings
        training_settings = [
            ("SpinBox", ("Max Runs", (30, 100, 1), 50)),
            ("SpinBox", ("Max Episodes", *run_settings["Episodes"])),
            ("SpinBox", ("Max Turns", *run_settings["Turns"]))
        ]
        # Widget lists
        widget_lists = [
            ("Environment Settings", environment_settings),
            ("Training Settings", training_settings)
        ]
        # Button labels
        button_labels = ["Others", "Back", "Parameters"]
        # Return frame, widgets and buttons
        return env_frame.create_gui_frame(widget_lists, button_labels)

    def get_parameter_frame(self, settings):
        # Create parameter subframe
        parameter_frame = FrameWidgets(self.main)
        # Load parameter settings
        parameter_settings = settings["Parameter"]
        # Load state spaces
        state_settings = settings["State"]
        # Get parameter settings
        parameters = [
            ("SpinBox", ("Q-Table Number", *parameter_settings["Q-Tables"])),
            ("SpinBox", ("Action Space", *parameter_settings["Action"])),
            ("OptionMenu", ("Q-Table Initialization", ["None", "Normal", "Uniform"], "None")),
            ("CheckButton", ("Opposition Learning", "Include", False)),
            ("OptionMenu", ("Reward Function", *parameter_settings["Reward"]))
        ]
        # Get state space
        state_space = [("SpinBox", state) for state in state_settings]
        # Widget lists
        widget_lists = [
            ("Parameter Settings", parameters),
            ("State Space", state_space)
        ]
        # Button labels
        button_labels = ["Tuning", "Back", "Experiment"]
        # Return frame, widgets and buttons
        return parameter_frame.create_gui_frame(widget_lists, button_labels)

    def get_other_frame(self, settings):
        # Load other settings
        other_settings = settings["Other"]
        # Check if other settings exists
        if other_settings is None:
            return None, None, None
        else:
            # Create other subframe
            other_frame = FrameWidgets(self.main)
            # Widget lists
            widget_lists = [
                ("Other Settings", other_settings)
            ]
            # Button labels
            button_labels = ["Back"]
            # Return frame, widgets and buttons
            return other_frame.create_gui_frame(widget_lists, button_labels)

    def get_experiment_frame(self, settings):
        # Create experiment subframe
        experiment_frame = FrameWidgets(self.main)
        # Load original results
        original_results = settings["Results"]
        # Return frame, widgets and buttons
        return experiment_frame.experiment_settings(original_results)

    def get_tune_frame(self):
        # Create tune subframe
        tune_frame = FrameWidgets(self.main)
        # Return frame, widgets and buttons
        return tune_frame.tune_settings()

    def get_settings_frame(self, main_settings):
        # Create settings subframe
        settings_frame = FrameWidgets(self.main)
        # Button labels
        button_labels = ["Other", "Results"]
        # Return frame and buttons
        return settings_frame.create_results_frame(main_settings, button_labels)

    def get_results_frame(self, exp_widgets, exp_results):
        # Create results subframe
        results_frame = FrameWidgets(self.main)
        # Button labels
        button_labels = ["Back", "Done"]
        # Return frame and buttons
        return results_frame.create_results_frame(exp_widgets + exp_results, button_labels)

    def get_hyperparameter_frame(self, tune_widgets, fittest_chromosomes):
        # Create hyperparameter subframe
        hyperparameter_frame = FrameWidgets(self.main)
        # Button labels
        button_labels = ["Back", "Done"]
        # Return frame and buttons
        return hyperparameter_frame.hyperparameter_results(tune_widgets, fittest_chromosomes, button_labels)

    def get_extra_frame(self, other_settings):
        # Check if other settings exists
        if other_settings is None:
            return None, None
        else:
            # Create other subframe
            other_frame = FrameWidgets(self.main)
            # Button labels
            button_labels = ["Back"]
            # Return frame and buttons
            return other_frame.create_results_frame(other_settings, button_labels)
