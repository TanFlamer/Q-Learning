from acrobot_settings import AcrobotSettings
from cartpole_settings import CartPoleSettings
from env_gui import EnvGUI


def link_button(button, first_frame, second_frame, open_frame=True):
    # Link button to command
    if open_frame:
        # Keep frame open
        button.configure(command=lambda: [first_frame.pack_forget(), second_frame.pack(fill='both', expand=1)])
    else:
        # Close frame for experiment
        button.configure(command=lambda: [first_frame.destroy()])


class GymEnv:
    def __init__(self):
        # Gym environment dictionary
        self.env_dict = {
            "Acrobot": AcrobotSettings().env_settings(),
            "CartPole": CartPoleSettings().env_settings()
        }

        # Gym environment list
        self.env_list = ["Acrobot", "CartPole"]
        self.default_env = "CartPole"

        # Create environment GUI
        self.env_gui = EnvGUI(self.env_list, self.default_env)

        # Environment frames
        self.initial_frame = None
        self.parameter_frame = None
        self.other_frame = None

        # Environment widgets
        self.initial_widgets = None
        self.parameter_widgets = None
        self.other_widgets = None

    def load_initial_frame(self, env):
        # Load run settings
        run_settings = self.env_dict[env]["Run"]
        # Create initial frame
        self.initial_frame, self.initial_widgets, initial_buttons = self.env_gui.get_initial_frame(run_settings)

    def load_parameter_frame(self, env):
        # Load parameter settings
        parameter_settings = self.env_dict[env]["Parameter"]
        # Load state spaces
        state_space = self.env_dict[env]["State"]
        # Create parameter frame
        self.parameter_frame, self.parameter_widgets, parameter_buttons = \
            self.env_gui.get_parameter_frame(parameter_settings, state_space)

    def load_other_frame(self, env):
        # Load other settings
        other_settings = self.env_dict[env]["Other"]
        # Create other frame
        self.other_frame, self.other_widgets, other_buttons = self.env_gui.get_other_frame(other_settings)

