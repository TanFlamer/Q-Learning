import math
import random
import numpy as np


def get_midpoints(obv):
    return get_midpoint(obv[0]) + get_midpoint(obv[1])


def get_midpoint(coordinates):
    return [(coordinates[0] + coordinates[2]) / 2, (coordinates[1] + coordinates[3]) / 2]


class QLearning:
    def __init__(self, parameter_settings, hyper_parameters, dimensions):
        # Unpack parameter settings
        [self.num_q_table, self.num_state, self.num_action,
         self.random_type, self.opposition, self.reward_type] = parameter_settings

        # Unpack hyper-parameters settings
        [self.learning_initial, self.learning_final, self.learning_step,
         self.explore_initial, self.explore_final, self.explore_step,
         self.discount_initial, self.discount_final, self.discount_step] = hyper_parameters

        # Canvas dimensions
        [self.width, self.height] = dimensions

        # Q-Learning counters
        self.turn = 0
        self.episode = 0
        self.runs = 0

        # Q-Learning variables
        self.q_tables = []
        self.state_0 = None
        self.terminated = None
        self.reward_function = None

        # Q-Learning fixed values
        self.buckets = (self.num_state * 2, self.num_action)
        self.max_dist = math.dist([self.width, self.height], [0, 0])

        # Q-Learning setup
        self.generate_tables()
        self.check_step_sign()
        self.assign_reward_function()

    def new_run(self):
        # Reset Q-tables
        self.generate_tables()
        # Increment run
        self.runs += 1
        # Reset episode
        self.episode = 0

    def new_episode(self, obv):
        # Increment episode
        self.episode += 1
        # Reset turn
        self.turn = 0
        # Get initial state
        self.state_0 = self.state_to_bucket(obv)

    def generate_tables(self):
        # Clear old Q-tables
        self.q_tables.clear()
        # Loop to create Q-tables
        for x in range(self.num_q_table):
            # Generate Q-Table
            q_table = self.single_table()
            # Append to Q-table list
            self.q_tables.append(q_table)

    def single_table(self):
        if self.random_type == "None":
            # Generate arrays of 0s
            return np.zeros(self.buckets)
        elif self.random_type == "Normal":
            # Generate arrays with normal distribution
            temp_table = np.random.randn(*self.buckets) * (10 / 3)
            # Bound arrays to range
            return np.clip(temp_table, -10, 10)
        else:
            # Generate arrays with uniform distribution
            return np.random.uniform(-10, 10, self.buckets)

    # Get bucket from state
    def state_to_bucket(self, obv):
        # Get midpoints
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        # Get bucket index
        diff_x = paddle_x - ball_x
        bucket = self.assign_bucket(abs(diff_x))
        bucket_index = self.num_state + bucket if diff_x >= 0 else (self.num_state - 1) - bucket
        # Return tuple
        return tuple([bucket_index])

    def assign_bucket(self, x):
        if x < 0:
            # First bucket
            return 0
        elif x >= self.width:
            # Last bucket
            return self.num_state - 1
        else:
            # Other buckets
            bucket_length = self.width / self.num_state
            return math.floor(x / bucket_length)

    def select_action(self):
        # Random action chance
        explore_rate = self.get_explore_rate()
        explore_action = random.random() < explore_rate
        # Available actions
        random_action = random.randint(0, self.num_action - 1)
        best_action = np.argmax(sum(self.q_tables)[self.state_0])
        # Select best or random action
        return random_action if explore_action else best_action

    def update_policy(self, obv, opposite_obv, action, terminated):
        # Increment turn
        self.turn += 1
        # Get Q-tables
        [main_q, secondary_q] = random.sample(self.q_tables, 2) if self.num_q_table > 1 else [self.q_tables[0]] * 2
        # Get terminated state
        self.terminated = terminated
        # Update Q-table
        self.update_table(main_q, secondary_q, obv, action)

        # Opposition learning
        if self.opposition and action <= 1:
            # Get opposite action
            opposite_action = 1 - action
            # Update opposite Q-table
            self.update_table(main_q, secondary_q, opposite_obv, opposite_action)

        # Save old state
        self.state_0 = self.state_to_bucket(obv)

    def update_table(self, main_table, secondary_table, obv, action):
        # Get hyper-parameters
        learning_rate = self.get_learning_rate()
        discount_factor = self.get_discount_factor()
        # Get state and reward
        state = self.state_to_bucket(obv)
        reward = self.reward_function(obv)
        # Update Q-table
        best_q = secondary_table[state + (np.argmax(main_table[state]),)]
        main_table[self.state_0 + (action,)] += learning_rate * (
                reward + discount_factor * best_q - main_table[self.state_0 + (action,)])

    def get_learning_rate(self):
        func, new_step = self.get_new_step(self.learning_step)
        return func(self.learning_initial + new_step, self.learning_final)

    def get_explore_rate(self):
        func, new_step = self.get_new_step(self.explore_step)
        return func(self.explore_initial + new_step, self.explore_final)

    def get_discount_factor(self):
        func, new_step = self.get_new_step(self.discount_step)
        return func(self.discount_initial + new_step, self.discount_final)

    def get_new_step(self, step):
        func = min if step >= 0 else max
        next_step = step * self.episode
        return func, next_step

    def check_step_sign(self):
        # Change step sign if initial greater than final value
        if self.learning_initial > self.learning_final: self.learning_step = -abs(self.learning_step)
        if self.explore_initial > self.explore_final: self.explore_step = -abs(self.explore_step)
        if self.discount_initial > self.discount_final: self.discount_step = -abs(self.discount_step)

    def assign_reward_function(self):
        if self.reward_type == "X-Distance":
            self.reward_function = self.x_distance
        elif self.reward_type == "X-Distance-Paddle":
            self.reward_function = self.x_distance_paddle
        elif self.reward_type == "Turn-Count":
            self.reward_function = self.turn_count
        elif self.reward_type == "XY-Distance":
            self.reward_function = self.xy_distance
        else:  # Constant-Reward
            self.reward_function = self.constant_reward

    def constant_reward(self, _):
        # Return 1 if not terminated else 0
        return 0 if self.terminated else 1

    def turn_count(self, _):
        # Return turn count
        return self.turn

    def x_distance(self, obv):
        [paddle_x, _, ball_x, _] = get_midpoints(obv)
        # Horizontal distance between midpoints of paddle and ball
        dist = abs(paddle_x - ball_x)
        # Shorter the distance, higher the reward
        return (self.width - dist) / 100

    def x_distance_paddle(self, obv):
        [x1, _, x2, _] = obv[0]  # Paddle coordinates
        [_, _, ball_x, _] = get_midpoints(obv)
        if x1 <= ball_x <= x2:
            # Max reward if ball is above paddle
            return self.width / 100
        else:
            # Horizontal distance between whole paddle and midpoint of ball
            dist = x1 - ball_x if ball_x < x1 else ball_x - x2
            # Shorter the distance, higher the reward
            return (self.width - dist) / 100

    def xy_distance(self, obv):
        midpoints = get_midpoints(obv)
        paddle_mid, ball_mid = midpoints[:2], midpoints[2:]
        # Euclidean distance between midpoints of paddle and ball
        dist = math.dist(paddle_mid, ball_mid)
        # Shorter the distance, higher the reward
        return (self.max_dist - dist) / 100
