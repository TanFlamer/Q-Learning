import math
import numpy as np


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


def future_position(obv):
    _, _, angle, velocity = obv
    threshold = math.pi / 15
    new_angle = angle + 0.02 * velocity
    terminated = new_angle < -threshold or new_angle > threshold
    return new_angle, terminated


def angle_reward(obv):
    angle, _ = future_position(obv)
    return max(math.pi / 15 - abs(angle), 0)


class CartpoleFunctions:
    def __init__(self, parameter_settings):
        # Step function constants
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.length = 0.5  # actually half the pole's length
        self.force_mag = 10.0
        # State bounds
        self.state_bounds = [(-4.8, 4.8), (-0.5, 0.5),
                             (-math.radians(24), math.radians(24)), (-math.radians(50), math.radians(50))]
        # Failure threshold
        self.x_threshold = 2.4
        self.theta_threshold_radians = math.pi / 15
        # Unpack parameter settings
        [_, self.num_state, _, _, self.opposition, self.reward_type] = parameter_settings

    def step_function(self, state, action):
        total_mass = self.masspole + self.masscart
        polemass_length = self.masspole * self.length
        tau = 0.02  # seconds between state updates

        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        temp = (force + polemass_length * theta_dot ** 2 * sintheta) / total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
                self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / total_mass))
        xacc = temp - polemass_length * thetaacc * costheta / total_mass

        x = x + tau * x_dot
        x_dot = x_dot + tau * xacc
        theta = theta + tau * theta_dot
        theta_dot = theta_dot + tau * thetaacc

        # New state
        state = (x, x_dot, theta, theta_dot)

        # Terminated
        terminated = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        return np.array(state, dtype=np.float32), terminated

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
        opposite_action = 1 - action if self.opposition else None
        return action, opposite_action

    def success_function(self, _, time_steps):
        return get_average(time_steps) >= 195.0

    def reward_function(self):

        # Return base reward
        def base_reward(_0, _1, _2): return 1
        # Penalise if action leads to termination
        def termination_penalty(obv, terminated, _): return -1 if terminated or future_position(obv)[1] else 1
        # Exponential reward based on turn
        def time_reward(_0, _1, turn): return math.exp(turn / 100)
        # Uniform reward based on angle
        def uniform_reward(obv, _0, _1): return 10 * angle_reward(obv)
        # Exponential reward based on angle
        def exponential_reward(obv, _0, _1): return 10 * math.exp(angle_reward(obv) - 1)
        # Logarithmic reward based on angle
        def logarithmic_reward(obv, _0, _1): return 10 * math.log(1 + angle_reward(obv))

        # Use dict to store functions
        functions = {"Base": base_reward, "Termination": termination_penalty, "Time": time_reward,
                     "Uniform": uniform_reward, "Exponential": exponential_reward, "Logarithmic": logarithmic_reward}
        # Return reward function
        return functions[self.reward_type]

