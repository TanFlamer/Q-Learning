import math
import cartpole_template as cartpole


# Base reward function for cartpole
def base_reward(reward):
    return reward


# Returns reward of -1 if action leads to termination
def termination_penalty(reward, obv, terminated):
    if terminated:
        return -reward
    else:
        _, future_terminated = future_position(obv)
        return reward if not future_terminated else -reward


# Returns reward based on current time step
# Reward increases exponentially with time
def time_reward(time):
    return math.exp(time / 100)


# Returns reward based on angle
# Reward varies linearly with angle
def uniform_reward(obv):
    angle, _ = future_position(obv)
    reward = 10 * max(math.pi / 15 - abs(angle), 0)
    return reward


# Returns reward based on angle
# Reward increases more rapidly as angle decreases
def exponential_reward(obv):
    angle, _ = future_position(obv)
    score = max(math.pi / 15 - abs(angle), 0)
    reward = 10 * (math.exp(score) - 1)
    return reward


# Returns reward based on angle
# Reward decreases more rapidly as angle increases
def logarithmic_reward(obv):
    angle, _ = future_position(obv)
    score = max(math.pi / 15 - abs(angle), 0)
    reward = 10 * (math.log(1 + score))
    return reward


# Get future position of cartpole based on current trajectory
def future_position(obv):
    _, _, angle, velocity = obv
    threshold = math.pi / 15
    new_angle = angle + 0.02 * velocity
    terminated = new_angle < -threshold or new_angle > threshold
    return new_angle, terminated


# Use the supplied reward function in runs
def reward_function(env_information):
    # Reward function
    obv, reward, terminated, time = env_information
    # Change reward function here
    return base_reward(reward)


# Experimental settings
if __name__ == "__main__":

    # t-test
    # Disclaimer: The t-test was implemented after results were calculated using fixed values
    #             with only 2 decimal places. Values returned by the new t-test may differ
    #             from old t-test values by up to 0.01. There is no error in the code.

    # Confidence level of one-tailed T-test (Original = 0.99)
    confidence_level = 0.99
    # Sample mean to be compared (Original = 257.27)
    sample_mean = 257.27
    # Sample standard deviation to be compared (Original = 14.94)
    sample_std = 14.94
    # Sample size to be compared (Original = 30)
    sample_size = 30

    # Improvements to Cartpole
    # Values used in the experiment can be changed below
    # First value is the default value

    # Number of Q-tables (Values = 1, 2, 3, 4, 5)
    num_tables = 1

    # Granularity of the state space (Values = (1, 1, 6, 3), (1, 1, 6, 7))
    num_buckets = (1, 1, 6, 3)

    # Initial Q-table values (Values = 0, 1)
    # Q-tables are initially filled with values from a standard normal distribution
    # Then the Q-tables are multiplied by the initial_q_table value
    # Setting initial_q_table to 0 produces Q-tables filled with 0s
    initial_q_table = 0

    # Opposite Q-Learning (Values = False, True)
    opposite_q_learning = False

    # Discount factor discounting (Values = True, False)
    # Setting it to True invalidates the following values
    fixed_discount_factor = True

    # Minimum discount factor (Value = 0.99)
    min_discount_factor = 0.99

    # Steps needed to reach discount factor of 1 (Value = 100)
    # Calculates step size to be increased each episode
    # Calculations = (1 - min_discount_factor) / discount_steps
    # Example = (1 - 0.99) / 100 = 0.0001 step size
    discount_steps = 100

    # Run settings
    variables = (num_tables, num_buckets, initial_q_table, opposite_q_learning)
    discount_settings = (fixed_discount_factor, min_discount_factor, discount_steps)
    run_settings = (variables, discount_settings)
    t_test_values = (confidence_level, sample_mean, sample_std, sample_size)

    # Run cartpole
    cartpole.run_simulation(run_settings, reward_function, t_test_values)
