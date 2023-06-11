# Env settings
from settings.acrobot_settings import AcrobotSettings
from settings.cartpole_settings import CartPoleSettings
# Env functions
from functions.acrobot_functions import AcrobotFunctions
from functions.cartpole_functions import CartpoleFunctions
# Gym environment
from gui.gym_env import GymEnv

# Gym environment dictionary
env_dict = {
    "Acrobot-v1": (AcrobotSettings, AcrobotFunctions),
    "CartPole-v0": (CartPoleSettings, CartpoleFunctions)
}

# Default gym environment
default_env = "CartPole-v0"

if __name__ == '__main__':
    # Create gym env
    gym_env = GymEnv(env_dict, default_env)
    # Load gym frame
    gym_env.load_gym_frame()
