import math
from environments.functions.env_functions import EnvFunctions


class BrickBreakerFunctions(EnvFunctions):
    def __init__(self, parameter_settings, other_settings):
        # Unpack parameter settings
        super().__init__(parameter_settings)

        # Ball settings
        self.ball_speed = other_settings["ball_speed"]
        self.radius = 10

        # Paddle settings
        self.paddle_speed = other_settings["paddle_speed"]
        self.paddle_movement = {0: -self.paddle_speed, 1: 0, 2: self.paddle_speed}
        self.half_width = 40

        # Get screen dimensions
        self.screen_width = 600
        self.screen_height = 450

        # Other settings
        self.max_dist = math.dist([self.screen_width, self.screen_height], [0, 0])
        self.game_mode = other_settings["game_mode"]

    def step_function(self, obv, action):
        # Unpack obv
        [paddle_center_x, paddle_center_y, ball_center_x, ball_center_y, horizontal, vertical, brick_count] = obv

        # Move paddle
        paddle_left, paddle_right = paddle_center_x - self.half_width, paddle_center_x + self.half_width
        paddle_x = self.paddle_movement[action]

        paddle_x = min(self.screen_width - paddle_right, paddle_x) if paddle_x >= 0 else -min(paddle_left, abs(paddle_x))
        paddle_center_x += paddle_x

        # Move ball
        ball_left, ball_right = ball_center_x - self.radius, ball_center_x + self.radius
        ball_top, ball_bottom = ball_center_y - self.radius, ball_center_y + self.radius
        ball_x, ball_y = self.ball_speed * (horizontal - 1), self.ball_speed * (vertical - 1)

        ball_x = min(self.screen_width - ball_right, ball_x) if ball_x >= 0 else -min(ball_left, abs(ball_x))
        ball_y = min(self.screen_height - ball_bottom, ball_y) if ball_y >= 0 else -min(ball_top, abs(ball_y))

        ball_center_x += ball_x
        ball_center_y += ball_y

        # Return new obv
        return [paddle_center_x, paddle_center_y, ball_center_x, ball_center_y,
                horizontal, vertical, brick_count], False

    def state_to_bucket(self, obv):
        # Unpack obv
        [paddle_center_x, paddle_center_y, ball_center_x, ball_center_y, horizontal, vertical, _] = obv

        # Get horizontal difference
        diff_x = paddle_center_x - ball_center_x
        state_x = self.num_state[0] // 2
        length_x = self.screen_width / state_x
        bucket_x = math.floor(abs(diff_x) / length_x)
        distance_x = state_x + bucket_x if diff_x >= 0 else (state_x - 1) - bucket_x

        # Get vertical difference
        diff_y = paddle_center_y - ball_center_y
        length_y = self.screen_height / self.num_state[1]
        distance_y = math.floor(abs(diff_y) / length_y)

        # Get ball horizontal direction
        ball_x = 0 if self.num_state[2] == 1 or horizontal == 0 else 1

        # Get ball vertical direction
        ball_y = 0 if self.num_state[3] == 1 or vertical == 0 else 1

        # Assign bucket
        return tuple([distance_x, distance_y, ball_x, ball_y])

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

    def success_function(self, _0, _1, obv):
        # Unpack obv
        [_, _, _, ball_center_y, _, vertical, _] = obv

        # Get ball points and offset
        ball_top, ball_bottom = ball_center_y - self.radius, ball_center_y + self.radius
        offset = vertical * self.ball_speed

        # Check for success
        return ball_top + offset > 0 if self.game_mode else ball_bottom + offset < self.screen_height

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
            [paddle_center_x, _, ball_center_x, _, _, _, _] = obv

            # Get paddle points
            paddle_left = paddle_center_x - self.half_width
            paddle_right = paddle_center_x + self.half_width

            # Ball is above paddle
            if paddle_left <= ball_center_x <= paddle_right:
                # Max reward
                return self.screen_width / 100
            else:
                # Horizontal distance between whole paddle and midpoint of ball
                dist = paddle_left - ball_center_x if ball_center_x < paddle_left else ball_center_x - paddle_right
                # Shorter the distance, higher the reward
                return (self.screen_width - dist) / 100

        # Use dict to store functions
        functions = {"Constant": constant_reward, "Turn-Count": turn_count, "X-Distance": x_distance,
                     "XY-Distance": xy_distance, "X-Distance-Paddle": x_distance_paddle}

        # Return reward function
        return functions[self.reward_type]
