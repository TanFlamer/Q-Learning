import numpy as np
from numpy import pi, radians, sin, cos, exp, log
from environments.functions.env_functions import EnvFunctions


def get_average(time_steps):
    # Number of elements
    num_elements = min(len(time_steps), 100)
    # Get average of last 100 elements
    return sum(time_steps[-num_elements:]) / num_elements


def future_position(obv):
    _, _, angle, velocity = obv
    threshold = pi / 15
    new_angle = angle + 0.02 * velocity
    terminated = new_angle < -threshold or new_angle > threshold
    return new_angle, terminated


def angle_reward(obv):
    angle, _ = future_position(obv)
    return max(pi / 15 - abs(angle), 0)


class CartpoleFunctions(EnvFunctions):
    def __init__(self, parameter_settings, _):
        # Unpack parameter settings
        super().__init__(parameter_settings)
        # Step function constants
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.length = 0.5  # actually half the pole's length
        self.force_mag = 10.0
        # Failure threshold
        self.x_threshold = 2.4
        self.theta_threshold_radians = pi / 15
        # State bounds
        self.state_bounds = [(-4.8, 4.8), (-0.5, 0.5), (-radians(24), radians(24)), (-radians(50), radians(50))]

    def step_function(self, obv, action):
        total_mass = self.masspole + self.masscart
        polemass_length = self.masspole * self.length
        tau = 0.02  # seconds between state updates

        x, x_dot, theta, theta_dot = obv
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = cos(theta)
        sintheta = sin(theta)

        temp = (force + polemass_length * theta_dot ** 2 * sintheta) / total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
                self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / total_mass))
        xacc = temp - polemass_length * thetaacc * costheta / total_mass

        x = x + tau * x_dot
        x_dot = x_dot + tau * xacc
        theta = theta + tau * theta_dot
        theta_dot = theta_dot + tau * thetaacc

        # New state
        obv = (x, x_dot, theta, theta_dot)

        # Terminated
        terminated = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        return np.array(obv, dtype=np.float32), terminated

    def state_to_bucket(self, obv):
        bucket_indices = []
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
            bucket_indices.append(bucket_index)
        return tuple(bucket_indices)

    def action_function(self, q_action):
        # Get actions
        opposite_q_action = 1 - q_action if self.opposition else None
        action = q_action
        opposite_action = opposite_q_action
        # Return actions
        return opposite_q_action, action, opposite_action

    def success_function(self, success_variables):
        time_steps, _, _ = success_variables
        return get_average(time_steps) >= 195.0

    def reward_function(self):

        # Return base reward
        def base_reward(_0, _1, _2): return 1
        # Penalise if action leads to termination
        def termination_penalty(obv, terminated, _): return -1 if terminated or future_position(obv)[1] else 1
        # Exponential reward based on turn
        def time_reward(_0, _1, turn): return exp(turn / 100)
        # Uniform reward based on angle
        def uniform_reward(obv, _0, _1): return 10 * angle_reward(obv)
        # Exponential reward based on angle
        def exponential_reward(obv, _0, _1): return 10 * exp(angle_reward(obv) - 1)
        # Logarithmic reward based on angle
        def logarithmic_reward(obv, _0, _1): return 10 * log(1 + angle_reward(obv))

        # Use dict to store functions
        functions = {"Base": base_reward, "Termination": termination_penalty, "Time": time_reward,
                     "Uniform": uniform_reward, "Exponential": exponential_reward, "Logarithmic": logarithmic_reward}
        # Return reward function
        return functions[self.reward_type]

