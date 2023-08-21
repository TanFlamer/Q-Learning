import math
import acrobot_template as acrobot


# Base reward function for acrobot
def base_reward(reward):
    return reward


# Returns reward based on current time step
# Reward decreases exponentially with time
# Reward of 0 is return if terminated
def time_penalty(time, reward, terminated):
    penalty = -math.exp(time / 200)
    return reward if terminated else penalty


# Returns reward based on velocity of joints
# Reward decreases when velocity decreases
# Reward decreases when velocity of both joints are in opposite directions
# Reward of 0 is return if terminated
def velocity_reward(obv, reward, terminated):
    _, _, _, _, velocity1, velocity2 = obv
    penalty = abs(velocity1 + velocity2) - 13 * math.pi
    return reward if terminated else penalty


# Returns reward based on height of free end
# Reward decreases when height decreases
# Reward of 0 is return if terminated
def height_reward(obv, reward, terminated):
    # Termination = -cos(a) - cos(a + b) > 1.0
    #  cos(a + b) = cos(a) * cos(b) - sin(a) * sin(b)
    # -cos(a) - cos(a + b) = sin(a) * sin(b) - cos(a) * (cos(b) + 1)
    cosA, sinA, cosB, sinB, _, _ = obv
    # Add -2 term to move range of results from -2 - 2 to -4 - 0
    penalty = sinA * sinB - cosA * (cosB + 1) - 2
    return reward if terminated else penalty


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
    # Sample mean to be compared (Original = 293.87)
    sample_mean = 293.87
    # Sample standard deviation to be compared (Original = 36.64)
    sample_std = 36.64
    # Sample size to be compared (Original = 30)
    sample_size = 30

    # Improvements to Acrobot
    # Values used in the experiment can be changed below
    # First value is the default value

    # Number of Q-tables (Values = 1, 2, 3, 4, 5)
    num_tables = 1

    # Granularity of the state space (Values = (1, 1, 1, 1, 10, 10))
    num_buckets = (1, 1, 1, 1, 10, 10)

    # Number of actions in action space (Values = 3, 2)
    num_actions = 3

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
    variables = (num_tables, num_buckets, num_actions, initial_q_table, opposite_q_learning)
    discount_settings = (fixed_discount_factor, min_discount_factor, discount_steps)
    run_settings = (variables, discount_settings)
    t_test_values = (confidence_level, sample_mean, sample_std, sample_size)

    # Run acrobot
    acrobot.run_simulation(run_settings, reward_function, t_test_values)
