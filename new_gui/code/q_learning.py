import random
import numpy as np


class QLearning:
    def __init__(self, parameter_settings):
        # Unpack parameter settings
        [self.num_q_table, self.num_state, self.num_action, self.random_type, _, _] = parameter_settings
        self.buckets = (self.num_state, self.num_action)

        # Counters
        self.runs = None
        self.episodes = None

        # Q-Tables
        self.q_tables = []
        self.state_0 = None
        self.main_table = None
        self.secondary_table = None

        # Learning rate
        self.learning_initial = None
        self.learning_final = None
        self.learning_step = None
        self.learning_rate = None

        # Explore rate
        self.explore_initial = None
        self.explore_final = None
        self.explore_step = None
        self.explore_rate = None

        # Discount factor
        self.discount_initial = None
        self.discount_final = None
        self.discount_step = None
        self.discount_factor = None

    def reset_agent(self, hyperparameters):
        # Reset runs
        self.runs = 0
        # Unpack hyperparameters settings
        [self.learning_initial, self.learning_final, self.learning_step,
         self.explore_initial, self.explore_final, self.explore_step,
         self.discount_initial, self.discount_final, self.discount_step] = hyperparameters
        # Check hyperparameter sign
        self.check_step_sign()

    def new_run(self):
        # Increment run
        self.runs += 1
        # Reset episode
        self.episodes = 0
        # Reset Q-tables
        self.generate_tables()

    def new_episode(self, state):
        # Increment episode
        self.episodes += 1
        # Get initial state
        self.state_0 = state
        # Set hyperparameters
        self.set_hyperparameters()

    def set_hyperparameters(self):
        self.learning_rate = self.get_learning_rate()
        self.explore_rate = self.get_explore_rate()
        self.discount_factor = self.get_discount_factor()

    def generate_tables(self):
        # Clear old Q-tables
        self.q_tables.clear()
        # Loop to create Q-tables
        for x in range(self.num_q_table):
            # Return single table
            q_table = self.single_table()
            # Append to Q-table list
            self.q_tables.append(q_table)

    def single_table(self):
        # Assign Q-table value
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

    def select_action(self):
        # Available actions
        random_action = random.randint(0, self.num_action - 1)
        best_action = np.argmax(sum(self.q_tables)[self.state_0])
        # Select best or random action
        return random_action if random.random() < self.explore_rate else best_action

    def select_tables(self):
        # Select Q-tables
        if len(self.q_tables) > 1:
            [self.main_table, self.secondary_table] = random.sample(self.q_tables, 2)
        else:
            [self.main_table, self.secondary_table] = [self.q_tables[0]] * 2

    def update_table(self, state, action, reward):
        # Get best Q-value
        best_q = self.secondary_table[state + (np.argmax(self.main_table[state]),)]
        # Update Q-table
        self.main_table[self.state_0 + (action,)] += self.learning_rate * (
                reward + self.discount_factor * best_q - self.main_table[self.state_0 + (action,)])

    def save_state(self, state):
        # Save old state
        self.state_0 = state

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
        next_step = step * self.episodes
        return func, next_step

    def check_step_sign(self):
        # Change step sign if initial greater than final value
        if self.learning_initial > self.learning_final: self.learning_step = -abs(self.learning_step)
        if self.explore_initial > self.explore_final: self.explore_step = -abs(self.explore_step)
        if self.discount_initial > self.discount_final: self.discount_step = -abs(self.discount_step)
