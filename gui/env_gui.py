# Import the required Libraries
from tkinter import Tk
from settings.frame_widgets import FrameWidgets


class EnvGUI:
    def __init__(self):
        # Create main window
        self.main = Tk()
        # Set the geometry of Tkinter frame
        self.main.title("Brick Breaker")
        self.main.geometry("600x450")

    def get_gym_frame(self, env_list, default_env):
        # Create gym subframe
        gym_frame = FrameWidgets(self.main)
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

    def get_env_frame(self, run_settings):
        # Create initial subframe
        env_frame = FrameWidgets(self.main)
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

    def get_parameter_frame(self, parameter_settings, state_settings):
        # Create parameter subframe
        parameter_frame = FrameWidgets(self.main)
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

    def get_other_frame(self, other_settings):
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

    def get_experiment_frame(self, original_results):
        # Create experiment subframe
        experiment_frame = FrameWidgets(self.main)
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

    def get_results_frame(self, exp_settings, results):
        # Create results subframe
        results_frame = FrameWidgets(self.main)
        # Button labels
        button_labels = ["Back", "Done"]
        # Return frame and buttons
        return results_frame.create_results_frame(exp_settings + results, button_labels)

    def get_hyperparameter_frame(self, tune_settings, fittest_chromosomes):
        # Create hyperparameter subframe
        hyperparameter_frame = FrameWidgets(self.main)
        # Button labels
        button_labels = ["Back", "Done"]
        # Return frame and buttons
        return hyperparameter_frame.hyperparameter_results(tune_settings, fittest_chromosomes, button_labels)

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
