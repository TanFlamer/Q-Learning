from .env_settings import EnvSettings


class CartPoleSettings(EnvSettings):
    def get_run_settings(self):
        run_settings = {
            "Episodes": ((200, 500, 50), 200),
            "Turns": ((200, 500, 50), 500)
        }
        return run_settings

    def get_parameter_settings(self):
        reward_list = ["Base", "Termination", "Time", "Uniform", "Exponential", "Logarithmic"]
        parameter_settings = {
            "Q-Tables": ((1, 5, 1), 1),
            "Action": ((2, 2, 1), 2),
            "Reward": (reward_list, "Base")
        }
        return parameter_settings

    def get_state_space(self):
        state_space = [
            ("Cart Position", (1, 10, 1), 1),
            ("Cart Velocity", (1, 10, 1), 1),
            ("Pole Angle", (1, 10, 1), 6),
            ("Pole Velocity", (1, 10, 1), 7)
        ]
        return state_space

    def get_other_settings(self):
        return None

    def get_original_results(self):
        original_results = {
            "Mean": 257.27,
            "STD": 14.94,
            "Size": 30
        }
        return original_results
