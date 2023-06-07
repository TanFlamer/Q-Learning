from env_settings import EnvSettings


class AcrobotSettings(EnvSettings):
    def get_run_settings(self):
        run_settings = {
            "Episodes": (200, 500, 50, 500),
            "Turns": (200, 500, 50, 500)
        }
        return run_settings

    def get_parameter_settings(self):
        reward_list = ["Base", "Time", "Velocity", "Height"]
        parameter_settings = {
            "Q-Tables": ((1, 5, 1), 1),
            "Action": ((2, 3, 1), 3),
            "Reward": (reward_list, "Base")
        }
        return parameter_settings

    def get_state_space(self):
        state_space = [
            ("Theta1 Cos", (1, 20, 1), 1),
            ("Theta1 Sin", (1, 20, 1), 1),
            ("Theta2 Cos", (1, 20, 1), 1),
            ("Theta2 Sin", (1, 20, 1), 1),
            ("Theta1 Velocity", (1, 20, 1), 10),
            ("Theta2 Velocity", (1, 20, 1), 10)
        ]
        return state_space

    def get_other_settings(self):
        return None

    def get_original_results(self):
        original_results = {
            "Mean": 293.87,
            "STD": 36.64,
            "Size": 30
        }
        return original_results
