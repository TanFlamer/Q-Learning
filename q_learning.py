import random
import numpy as np


class QLearning:
    def __init__(self, hyper_parameters):
        # Unpack hyper-parameters settings
        [self.learning_initial, self.learning_final, self.learning_step,
         self.explore_initial, self.explore_final, self.explore_step,
         self.discount_initial, self.discount_final, self.discount_step] = hyper_parameters

        # Q-Learning counters
        self.turn = 0
        self.episode = 0
        self.runs = 0

        # Q-Learning variables
        self.q_tables = []
        self.state_0 = None
        self.main_table = None
        self.secondary_table = None
        self.check_step_sign()

    def new_run(self, table_settings):
        # Reset Q-tables
        self.generate_tables(table_settings)
        # Increment run
        self.runs += 1
        # Reset episode
        self.episode = 0

    def new_episode(self, state):
        # Increment episode
        self.episode += 1
        # Reset turn
        self.turn = 0
        # Get initial state
        self.state_0 = state

    def generate_tables(self, table_settings):
        # Unpack table settings
        [num_q_table, random_type, buckets] = table_settings
        # Clear old Q-tables
        self.q_tables.clear()
        # Loop to create Q-tables
        for x in range(num_q_table): self.single_table(random_type, buckets)

    def single_table(self, random_type, buckets):
        # Assign Q-table value
        if random_type == "None":
            # Generate arrays of 0s
            q_table = np.zeros(buckets)
        elif random_type == "Normal":
            # Generate arrays with normal distribution
            temp_table = np.random.randn(*buckets) * (10 / 3)
            # Bound arrays to range
            q_table = np.clip(temp_table, -10, 10)
        else:
            # Generate arrays with uniform distribution
            q_table = np.random.uniform(-10, 10, buckets)
        # Append to Q-table list
        self.q_tables.append(q_table)

    def select_action(self, num_action):
        # Random action chance
        explore_rate = self.get_explore_rate()
        explore_action = random.random() < explore_rate
        # Available actions
        random_action = random.randint(0, num_action - 1)
        best_action = np.argmax(sum(self.q_tables)[self.state_0])
        # Select best or random action
        return random_action if explore_action else best_action

    def select_tables(self):
        # Increment turn
        self.turn += 1
        # Select Q-tables
        if len(self.q_tables) > 1:
            [self.main_table, self.secondary_table] = random.sample(self.q_tables, 2)
        else:
            [self.main_table, self.secondary_table] = [self.q_tables[0]] * 2

    def update_table(self, state, action, reward):
        # Get hyper-parameters
        learning_rate = self.get_learning_rate()
        discount_factor = self.get_discount_factor()
        # Update Q-table
        best_q = self.secondary_table[state + (np.argmax(self.main_table[state]),)]
        self.main_table[self.state_0 + (action,)] += learning_rate * (
                reward + discount_factor * best_q - self.main_table[self.state_0 + (action,)])

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
        next_step = step * self.episode
        return func, next_step

    def check_step_sign(self):
        # Change step sign if initial greater than final value
        if self.learning_initial > self.learning_final: self.learning_step = -abs(self.learning_step)
        if self.explore_initial > self.explore_final: self.explore_step = -abs(self.explore_step)
        if self.discount_initial > self.discount_final: self.discount_step = -abs(self.discount_step)
