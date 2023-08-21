# Adapted from: https://medium.com/@tuzzer/cart-pole-balancing-with-q-learning-b54c6068d947
from gym.envs.classic_control.acrobot import wrap, bound, rk4
from numpy import cos, pi, sin

import results_processing
import math
import random
import gym
import numpy as np

# Initialize the "Acrobot" environment
env = gym.make('Acrobot-v1')

# Random seed
RANDOM_SEED = 20313854

# Bounds for each discrete state
STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))

# Defining the simulation related constants
NUM_TRAIN_EPISODES = 500
MAX_TRAIN_T = 500

# Run settings
MIN_RUNS = 30
MAX_RUNS = 50

# Hyper parameters
MAX_DISCOUNT_FACTOR = 0.999
MIN_LEARNING_RATE = 0.1
MIN_EXPLORE_RATE = 0.01


# Loop through runs to collect results
def loop(run_settings, reward_function, t_test_values):
    episodes = []
    failed_runs = []
    run_number = 0
    # Loop through runs until at least 30 runs or at most 50 runs
    while len(episodes) < MIN_RUNS and run_number < MAX_RUNS:
        run_number += 1
        episode, solved = train(run_number, run_settings, reward_function)
        if solved:
            # Record number of episodes if run succeeds
            episodes.append(episode)
        else:
            # Record failure if run fails
            failed_runs.append(run_number)
            print("Run %2d failed in %d episodes - *" % (run_number, NUM_TRAIN_EPISODES))
    # Return results after processing
    return results_processing.get_results(episodes, t_test_values), failed_runs


def train(run, run_settings, reward_function):
    # Unpacking run settings
    variables, discount_settings = run_settings

    # Unpacking variables
    num_tables, num_buckets, num_actions, initial_q_table, opposite_q_learning = variables

    # Unpacking discount settings
    fixed_discount_factor, min_discount_factor, discount_steps = discount_settings

    # Discount step size
    discount_step_size = (1 - min_discount_factor) / discount_steps

    # Instantiating the learning related parameters
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)

    # Q-tables list
    q_tables = []

    # Fill Q-tables with initial values
    for x in range(num_tables):
        q_tables.append(np.zeros(num_buckets + (
            num_actions,)) if initial_q_table == 0 else np.random.randn(*num_buckets, num_actions) * initial_q_table)

    time_steps = [0]
    episodes_to_solve = 0
    solved = False

    # Run episode at most 500 times or solved requirements met
    for episode in range(1, NUM_TRAIN_EPISODES + 1):

        # Reset the environment
        obv, _ = env.reset()

        # the initial state
        state_0 = state_to_bucket(obv, num_buckets)

        # Get discount factor
        discount_factor = MAX_DISCOUNT_FACTOR if fixed_discount_factor else min(
            min_discount_factor + discount_step_size * episode, MAX_DISCOUNT_FACTOR)

        # Run at most 500 time steps or termination conditions met
        for t in range(1, MAX_TRAIN_T + 1):
            env.render()

            # Save old state for opposition learning
            old_obv = env.state

            # Select an action
            action = select_action(state_0, explore_rate, q_tables, num_actions)
            # Get opposite action
            opposite_action = num_actions - action - 1
            # Check if Opposite Q-Learning is valid
            # If do nothing action is chosen, no opposite action exists
            opposite_q_learning_pass = opposite_q_learning and action != opposite_action

            # Get Q-table index to be updated
            index_main = 0
            # Get Q-table index to get best Q-value
            index_secondary = 0
            # Get Q-tables count
            q_table_length = len(q_tables)

            # If more than 1 Q-table, get different Q-table indexes
            # Else use same Q-table
            if q_table_length > 1:
                # Get first Q-table index
                index_main = random.randint(0, q_table_length - 1)
                # Get second Q-table index
                index_secondary = random.randint(0, q_table_length - 2)
                # Move second Q-table index if overlap occurs
                index_secondary += 1 if index_secondary >= index_main else 0

            # Get first Q-table
            q_table_main = q_tables[index_main]
            # Get second Q-table
            q_table_secondary = q_tables[index_secondary]

            # Execute the action
            obv, reward, terminated, _, _ = env.step(action if num_actions == 3 else action * 2)

            # Observe the result
            state = state_to_bucket(obv, num_buckets)

            # Get reward from reward function
            reward = reward_function((obv, reward, terminated, t))

            # Get best Q value
            best_q = q_table_secondary[state + (np.argmax(q_table_main[state]),)]

            if opposite_q_learning_pass:
                # Execute opposite action
                opposite_obv, opposite_reward, opposite_terminated, _, _ = step(
                    old_obv, opposite_action if num_actions == 3 else opposite_action * 2)

                # Observe opposite result
                opposite_state = state_to_bucket(opposite_obv, num_buckets)

                # Get opposite reward from reward function
                opposite_reward = reward_function((opposite_obv, opposite_reward, opposite_terminated, t))

                # Get opposite best Q value
                opposite_best_q = q_table_secondary[opposite_state + (np.argmax(q_table_main[opposite_state]),)]

                # Updating opposite Q table
                q_table_main[state_0 + (opposite_action,)] += learning_rate * (
                        opposite_reward + discount_factor * opposite_best_q - q_table_main[state_0 + (opposite_action,)])

            # Updating Q table
            q_table_main[state_0 + (action,)] += learning_rate * (
                    reward + discount_factor * best_q - q_table_main[state_0 + (action,)])

            # Termination
            if terminated:
                # Record time steps to termination cumulatively
                time_steps.append(t + time_steps[-1])
                break

            # Setting up for the next iteration
            state_0 = state

        else:
            # Record time steps to termination cumulatively
            time_steps.append(MAX_TRAIN_T + time_steps[-1])

        # It's considered done when average for last 100 time steps is <= 195.0
        average = results_processing.get_average(time_steps)

        if episode % 50 == 0:
            print("%d %f" % (episode, average))

        if average <= 195.0:
            episodes_to_solve = episode
            solved = True
            print("Run %2d solved in %d episodes" % (run, episode))
            break

        # Update parameters
        learning_rate = get_learning_rate(episode)
        explore_rate = get_explore_rate(episode)

    return episodes_to_solve, solved


# Select action based on sum of Q-tables or randomly
def select_action(state, explore_rate, q_tables, num_actions):
    # Select a random action
    if random.random() < explore_rate:
        action = env.action_space.sample() if num_actions == 3 else random.randint(0, 1)
    # Select the action with the highest q
    else:
        action = np.argmax(sum(q_tables)[state])
    return action


# Get explore rate based on episode
def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(1.0, 1.0 - math.log10((t + 1) / 25)))


# Get learning rate based on episode
def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.5, 1.0 - math.log10((t + 1) / 25)))


# Get bucket from state
def state_to_bucket(state, num_buckets):
    bucket_indices = []
    for i in range(len(state)):
        if state[i] <= STATE_BOUNDS[i][0]:
            bucket_index = 0
        elif state[i] >= STATE_BOUNDS[i][1]:
            bucket_index = num_buckets[i] - 1
        else:
            # Mapping the state bounds to the bucket array
            bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
            offset = (num_buckets[i] - 1) * STATE_BOUNDS[i][0] / bound_width
            scaling = (num_buckets[i] - 1) / bound_width
            bucket_index = int(round(scaling * state[i] - offset))
            # For easier visualization of the above, you might want to use
            # pen and paper and apply some basic algebraic manipulations.
            # If you do so, you will obtain (B-1)*[(S-MIN)]/W], where
            # B = NUM_BUCKETS, S = state, MIN = STATE_BOUNDS[i][0], and
            # W = bound_width. This simplification is very easily
            # to visualize, i.e. num_buckets x percentage in width.
        bucket_indices.append(bucket_index)
    return tuple(bucket_indices)


# Function copied from source code for opposition learning
def step(state, action):
    dt = 0.2

    MAX_VEL_1 = 4 * pi
    MAX_VEL_2 = 9 * pi

    AVAIL_TORQUE = [-1.0, 0.0, +1]
    torque = AVAIL_TORQUE[action]

    # Now, augment the state with our force action, so it can be passed to _dsdt
    s_augmented = np.append(state, torque)
    ns = rk4(_dsdt, s_augmented, [0, dt])

    ns[0] = wrap(ns[0], -pi, pi)
    ns[1] = wrap(ns[1], -pi, pi)
    ns[2] = bound(ns[2], -MAX_VEL_1, MAX_VEL_1)
    ns[3] = bound(ns[3], -MAX_VEL_2, MAX_VEL_2)

    state = ns
    terminated = bool(-cos(state[0]) - cos(state[1] + state[0]) > 1.0)
    reward = -1.0 if not terminated else 0.0

    return np.array([cos(state[0]), sin(state[0]), cos(state[1]), sin(state[1]), state[2], state[3]], dtype=np.float32
                    ), reward, terminated, False, {}


# Function copied from source code for opposition learning
def _dsdt(s_augmented):
    book_or_nips = "book"
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

    if book_or_nips == "nips":
        # the following line is consistent with the description in the paper
        ddtheta2 = (a + d2 / d1 * phi1 - phi2) / (m2 * lc2 ** 2 + I2 - d2 ** 2 / d1)
    else:
        # the following line is consistent with the java implementation and the book
        ddtheta2 = (a + d2 / d1 * phi1 - m2 * l1 * lc2 * dtheta1 ** 2 * sin(theta2) - phi2) / (
                m2 * lc2 ** 2 + I2 - d2 ** 2 / d1)

    ddtheta1 = -(d2 * ddtheta2 + phi1) / d1

    return dtheta1, dtheta2, ddtheta1, ddtheta2, 0.0


# Initialise all random number generator with give seed
def random_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    env.action_space.seed(seed)
    env.reset(seed=seed)


# Run acrobot
def run_simulation(run_settings, reward_function, t_test_values):
    random_seed(RANDOM_SEED)
    results, failed = loop(run_settings, reward_function, t_test_values)
    results_processing.print_results(results, failed)
