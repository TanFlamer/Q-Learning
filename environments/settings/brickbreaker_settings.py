from .env_settings import EnvSettings


class BrickBreakerSettings(EnvSettings):
    def get_run_settings(self):
        run_settings = {
            "Episodes": ((200, 500, 50), 200),
            "Turns": ((5000, 20000, 1000), 10000)
        }
        return run_settings

    def get_parameter_settings(self):
        reward_list = ["Constant", "Turn-Count", "X-Distance", "XY-Distance", "X-Distance-Paddle"]
        parameter_settings = {
            "Q-Tables": ((1, 5, 1), 1),
            "Action": ((2, 3, 1), 3),
            "Reward": (reward_list, "Constant")
        }
        return parameter_settings

    def get_state_space(self):
        state_space = [
            ("Horizontal Distance", (2, 20, 2), 2),
            ("Vertical Distance", (1, 10, 1), 1),
            ("Ball Horizontal", (1, 2, 1), 1),
            ("Ball Vertical", (1, 2, 1), 1)
        ]
        return state_space

    def get_other_settings(self):
        other_settings = [
            ("OptionMenu", ("Brick Placement", ["Row", "Column", "Random"], "Row")),
            ("SpinBox", ("Brick Rows", (1, 10, 1), 3)),
            ("OptionMenu", ("Brick Columns", [1, 2, 3, 4, 5, 6, 8, 10, 12, 15], 8)),
            ("SpinBox", ("Paddle Speed", (5, 15, 1), 10)),
            ("SpinBox", ("Ball Speed", (1, 10, 1), 5)),
            ("CheckButton", ("Game Mode", "Inverted", False))
        ]
        return other_settings

    def get_original_results(self):
        original_results = {
            "Mean": 45.63,
            "STD": 1.40,
            "Size": 30
        }
        return original_results
