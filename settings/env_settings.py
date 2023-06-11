from abc import ABC, abstractmethod


class EnvSettings(ABC):
    def env_settings(self):
        # Returns settings used in environment
        return {
            "Run": self.get_run_settings(),
            "State": self.get_state_space(),
            "Other": self.get_other_settings(),
            "Results": self.get_original_results(),
            "Parameter": self.get_parameter_settings()
        }

    @abstractmethod
    def get_run_settings(self):
        """Return episode and turn settings"""
        # run_settings = {
        #     "Episodes": (("Min", "Max", "Increment"), "Default"),
        #     "Turns": (("Min", "Max", "Increment"), "Default")
        # }

    @abstractmethod
    def get_parameter_settings(self):
        """Return parameter settings"""
        # parameter_settings = {
        #     "Q-Tables": (("Min", "Max", "Increment"), "Default"),
        #     "Action": (("Min", "Max", "Increment"), "Default"),
        #     "Reward": (["Option List"], "Default")
        # }

    @abstractmethod
    def get_state_space(self):
        """Return state space (Add as many lines as needed)"""
        # state_space = [
        #     ("Label", ("Min", "Max", "Increment"), "Default")
        # ]

    @abstractmethod
    def get_other_settings(self):
        """Return other settings (None if unused)"""
        # other_settings = [
        #     ("Entry", ("Label", "Default")),
        #     ("SpinBox", ("Label", ("Min", "Max", "Increment"), "Default")),
        #     ("OptionMenu", ("Label", ["Option List"], "Default")),
        #     ("CheckButton", ("Label", "Text", "Default"))
        # ]

    @abstractmethod
    def get_original_results(self):
        """Return original results to compare"""
        # original_results = {
        #     "Mean": float,
        #     "STD": float,
        #     "Size": int
        # }
