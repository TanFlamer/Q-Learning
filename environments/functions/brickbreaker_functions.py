import math
import numpy as np
from environments.functions.env_functions import EnvFunctions


class BrickBreakerFunctions(EnvFunctions):
    def __init__(self, parameter_settings, other_settings):
        # Unpack parameter settings
        super().__init__(parameter_settings)
        # Ball and paddle settings
        self.ball_speed = other_settings["ball_speed"]
        self.paddle_speed = other_settings["paddle_speed"]
        self.radius = 10
        self.half_width = 40
        # Get screen dimensions
        self.screen_width = 600
        self.screen_height = 450
        self.max_dist = math.dist([self.screen_width, self.screen_height], [0, 0])

    def step_function(self, obv, action):
        # Unpack obv
        [paddle_x, _, _, _, _] = obv
        # Move paddle
        paddle_movement = {0: -self.paddle_speed, 1: 0, 2: self.paddle_speed}
        offset = paddle_movement[action]
        offset = min(self.screen_width - paddle_x + self.half_width,
                     offset) if offset >= 0 else -min(paddle_x - self.half_width, abs(offset))
        obv[0] += offset
        # Return new obv
        return np.array(obv, dtype=np.float32), False

    def state_to_bucket(self, obv):
        # Unpack obv
        [paddle_x, paddle_y, ball_x, ball_y, _] = obv

        # Get horizontal difference
        diff_x = paddle_x - ball_x
        state_x = self.num_state[0] // 2
        length_x = self.screen_width / state_x
        bucket_x = math.floor(abs(diff_x) / length_x)
        index_x = state_x + bucket_x if diff_x >= 0 else (state_x - 1) - bucket_x

        # Get vertical difference
        diff_y = paddle_y - ball_y
        length_y = self.screen_height / self.num_state[1]
        index_y = math.floor(abs(diff_y) / length_y)

        # Assign bucket
        return tuple([index_x, index_y])

    def action_function(self, q_action):
        # Get actions
        if self.num_action == 2:
            opposite_q_action = 1 - q_action
            action = q_action * 2
            opposite_action = opposite_q_action * 2 if self.opposition else None
        else:
            opposite_q_action = 2 - q_action
            action = q_action
            opposite_action = opposite_q_action if self.opposition else None
        # Return actions
        return opposite_q_action, action, opposite_action

    def success_function(self, success_variables):
        # Unpack obv
        _, _, obv = success_variables
        [_, _, _, ball_y, _] = obv
        # Get ball points
        ball_top = ball_y - self.radius
        ball_bottom = ball_y + self.radius
        # Check for success
        return ball_top - self.ball_speed > 0 and ball_bottom + self.ball_speed < self.screen_height

    def reward_function(self):

        # Return constant reward
        def constant_reward(_0, _1, _2): return 1

        # Return turn count
        def turn_count(_0, _1, turn): return turn

        # Return horizontal distance
        def x_distance(obv, _0, _1): return (self.screen_width - abs(obv[0] - obv[2])) / 100

        # Return Euclidean distance
        def xy_distance(obv, _0, _1): return (self.max_dist - math.dist(obv[0:2], obv[2:4])) / 100

        # Shortest distance of ball from paddle
        def x_distance_paddle(obv, _0, _1):
            # Unpack obv
            [paddle_x, paddle_y, ball_x, ball_y, _] = obv
            # Get paddle points
            paddle_left = paddle_x - self.half_width
            paddle_right = paddle_x + self.half_width
            # Ball is above paddle
            if paddle_left <= ball_x <= paddle_right:
                # Max reward
                return self.screen_width / 100
            else:
                # Horizontal distance between whole paddle and midpoint of ball
                dist = paddle_left - ball_x if ball_x < paddle_left else ball_x - paddle_right
                # Shorter the distance, higher the reward
                return (self.screen_width - dist) / 100

        # Use dict to store functions
        functions = {"Constant": constant_reward, "Turn-Count": turn_count, "X-Distance": x_distance,
                     "XY-Distance": xy_distance, "X-Distance-Paddle": x_distance_paddle}
        # Return reward function
        return functions[self.reward_type]
