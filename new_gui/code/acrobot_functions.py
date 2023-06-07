import numpy as np
from numpy import pi, sin, cos, exp
from gym.envs.classic_control.acrobot import wrap, bound, rk4
from new_gui.code.env_functions import EnvFunctions


def get_average(time_steps):
    # Total number of elements
    num_elements = len(time_steps) - 1
    # Calculate average time steps
    if num_elements <= 100:
        # Divide current cumulative time steps if < 100
        return time_steps[-1] / num_elements
    else:
        # Divide last 100 cumulative time steps if >= 100
        return (time_steps[-1] - time_steps[-101]) / 100


def _dsdt(s_augmented):
    m1 = 1.0  #: [kg] mass of link 1
    m2 = 1.0  #: [kg] mass of link 2
    l1 = 1.0  # [m]
    lc1 = 0.5  #: [m] position of the center of mass of link 1
    lc2 = 0.5  #: [m] position of the center of mass of link 2
    I1 = 1.0  #: moments of inertia for both links
    I2 = 1.0  #: moments of inertia for both links
    g = 9.8

    a = s_augmented[-1]
    s = s_augmented[:-1]

    theta1 = s[0]
    theta2 = s[1]
    dtheta1 = s[2]
    dtheta2 = s[3]

    d1 = (m1 * lc1 ** 2 + m2 * (l1 ** 2 + lc2 ** 2 + 2 * l1 * lc2 * cos(theta2)) + I1 + I2)
    d2 = m2 * (lc2 ** 2 + l1 * lc2 * cos(theta2)) + I2

    phi2 = m2 * lc2 * g * cos(theta1 + theta2 - pi / 2.0)
    phi1 = (-m2 * l1 * lc2 * dtheta2 ** 2 * sin(theta2) - 2 * m2 * l1 * lc2 * dtheta2 * dtheta1 * sin(theta2)
            + (m1 * lc1 + m2 * l1) * g * cos(theta1 - pi / 2) + phi2)

    # the following line is consistent with the java implementation and the book
    ddtheta2 = (a + d2 / d1 * phi1 - m2 * l1 * lc2 * dtheta1 ** 2 * sin(theta2) - phi2) / (
            m2 * lc2 ** 2 + I2 - d2 ** 2 / d1)
    ddtheta1 = -(d2 * ddtheta2 + phi1) / d1

    return dtheta1, dtheta2, ddtheta1, ddtheta2, 0.0


class AcrobotFunctions(EnvFunctions):
    def __init__(self, parameter_settings):
        # Unpack parameter settings
        super().__init__(parameter_settings)
        # Step function constants
        self.MAX_VEL_1 = 4 * pi
        self.MAX_VEL_2 = 9 * pi
        self.AVAIL_TORQUE = [-1.0, 0.0, +1]
        # State bounds
        self.state_bounds = [(-1, 1), (-1, 1), (-1, 1), (-1, 1), (-4 * pi, 4 * pi), (-9 * pi, 9 * pi)]

    def step_function(self, obv, action):
        torque = self.AVAIL_TORQUE[action]

        # Now, augment the state with our force action, so it can be passed to _dsdt
        s_augmented = np.append(obv, torque)
        ns = rk4(_dsdt, s_augmented, [0, 0.2])

        ns[0] = wrap(ns[0], -pi, pi)
        ns[1] = wrap(ns[1], -pi, pi)
        ns[2] = bound(ns[2], -self.MAX_VEL_1, self.MAX_VEL_1)
        ns[3] = bound(ns[3], -self.MAX_VEL_2, self.MAX_VEL_2)

        # Termination
        terminated = bool(-cos(ns[0]) - cos(ns[1] + ns[0]) > 1.0)
        return np.array([cos(ns[0]), sin(ns[0]), cos(ns[1]), sin(ns[1]), ns[2], ns[3]], dtype=np.float32), terminated

    def state_to_bucket(self, obv):
        bucket_indice = []
        for i in range(len(obv)):
            if obv[i] <= self.state_bounds[i][0]:
                bucket_index = 0
            elif obv[i] >= self.state_bounds[i][1]:
                bucket_index = self.num_state[i] - 1
            else:
                # Mapping the state bounds to the bucket array
                bound_width = self.state_bounds[i][1] - self.state_bounds[i][0]
                offset = (self.num_state[i] - 1) * self.state_bounds[i][0] / bound_width
                scaling = (self.num_state[i] - 1) / bound_width
                bucket_index = int(round(scaling * obv[i] - offset))
            bucket_indice.append(bucket_index)
        return tuple(bucket_indice)

    def action_function(self, action):
        if self.num_action == 2: action = action * 2
        opposite_action = 2 - action if self.opposition and action != 1 else None
        return action, opposite_action

    def success_function(self, time_steps, _0, _1):
        return get_average(time_steps) <= 195.0

    def reward_function(self):

        # Return base reward
        def base_reward(_0, terminated, _1): return 0 if terminated else -1
        # Penalty based on turn
        def time_penalty(_, terminated, turn): return 0 if terminated else -exp(turn / 200)
        # Reward based on velocity
        def velocity_reward(obv, terminated, _): return 0 if terminated else abs(obv[4] + obv[5]) - 13 * pi
        # Reward based on height
        def height_reward(obv, terminated, _): return 0 if terminated else obv[1] * obv[3] - obv[0] * (obv[2] + 1) - 2

        # Use dict to store functions
        functions = {"Base": base_reward, "Time": time_penalty, "Velocity":velocity_reward, "Height": height_reward}
        # Return reward function
        return functions[self.reward_type]
