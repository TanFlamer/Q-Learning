# Env settings
from environments.settings.acrobot_settings import AcrobotSettings
from environments.settings.cartpole_settings import CartPoleSettings
from environments.settings.brickbreaker_settings import BrickBreakerSettings

# Env functions
from environments.functions.acrobot_functions import AcrobotFunctions
from environments.functions.cartpole_functions import CartpoleFunctions
from environments.functions.brickbreaker_functions import BrickBreakerFunctions

# Gym environment
from code.gym_control import GymControl
from gym.envs.registration import register

# Register brick breaker environment
register(
    id='BrickBreaker-v0',
    entry_point='environments.custom.brickbreaker:BrickBreakerEnv'
)

# Gym environment dictionary
env_dict = {
    "Acrobot-v1": (AcrobotSettings, AcrobotFunctions),
    "CartPole-v1": (CartPoleSettings, CartpoleFunctions),
    "BrickBreaker-v0": (BrickBreakerSettings, BrickBreakerFunctions)
}

# Default gym environment
default_env = "CartPole-v1"

if __name__ == '__main__':
    # Create gym env
    gym_control = GymControl()
    # Load gym frame
    gym_control.load_gui(env_dict, default_env)
