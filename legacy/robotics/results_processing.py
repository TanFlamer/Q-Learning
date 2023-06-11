import math
import numpy as np
import scipy


# Get average of last 100 time steps
def get_average(time_steps):
    num_elements = len(time_steps) - 1
    if num_elements <= 100:
        # If less than 100 time steps, divide current cumulative time steps
        average = time_steps[-1] / num_elements
    else:
        # If more than or equal to 100 time steps, divide last 100 cumulative time steps
        average = (time_steps[-1] - time_steps[-101]) / 100
    # Return average of last 100 time steps
    return average


# Get the median and inter quartile range
def get_quartiles(runs, episodes):
    episodes.sort()
    if runs % 2 == 0:
        midpoint = runs // 2 - 1
        median = (episodes[midpoint] + episodes[midpoint + 1]) / 2
        runs_halved = runs // 2
        offset = 0
    else:
        midpoint = (runs + 1) // 2 - 1
        median = episodes[midpoint]
        runs_halved = (runs - 1) // 2
        offset = 1

    if runs_halved % 2 == 0:
        midpoint = runs_halved // 2 - 1
        first_quartile = (episodes[midpoint] + episodes[midpoint + 1]) / 2
        third_quartile = (episodes[midpoint + runs_halved + offset] + episodes[
            midpoint + runs_halved + offset + 1]) / 2
    else:
        midpoint = (runs_halved + 1) // 2 - 1
        first_quartile = episodes[midpoint]
        third_quartile = episodes[midpoint + runs_halved + offset]
    # Return the median and inter quartile range
    return median, third_quartile - first_quartile


# Calculate the expected difference between the two samples using the t-test
def calculate_t_value(t_test_values, second_sample_results):
    # Unpack first sample data
    confidence_level, first_sample_mean, first_sample_std, first_sample_size = t_test_values
    # Unpack second sample data
    second_sample_mean, second_sample_std, second_sample_size = second_sample_results
    # Get difference in mean of both samples
    mean_difference = first_sample_mean - second_sample_mean
    # Get variance of first sample
    first_sample_variance = first_sample_std * first_sample_std
    # Get variance of second sample
    second_sample_variance = second_sample_std * second_sample_std
    # Get intermediate data of first sample
    first_sample_data = first_sample_variance * (first_sample_size - 1)
    # Get intermediate data of second sample
    second_sample_data = second_sample_variance * (second_sample_size - 1)
    # Get degrees of freedom of both samples
    degrees_of_freedom = first_sample_size + second_sample_size - 2
    # Get pooled variance from both samples
    pooled_variance = (first_sample_data + second_sample_data) / degrees_of_freedom
    # Get pooled standard deviation from both samples
    pooled_std = math.sqrt(pooled_variance)
    # Get critical value from confidence level and degrees of freedom
    critical_value = scipy.stats.t.ppf(confidence_level, degrees_of_freedom)
    # Calculate intermediate data of t-test
    t_test_bottom = pooled_std * math.sqrt(1 / first_sample_size + 1 / second_sample_size)
    # Calculate the expected difference between the two samples
    difference = mean_difference - critical_value * t_test_bottom
    # Return the expected difference between the two samples or 0 if t-test fails
    return max(difference, 0)


# Get results of experiment
def get_results(episodes, t_test_values):
    runs = len(episodes)
    if runs == 0:
        # Return all 0s for 0 runs
        return (0, 0, 0), (0, 0, 0, 0), 0
    elif runs == 1:
        # Return results for 1 run
        return (episodes[0], 0, 1), (episodes[0], 0, episodes[0], episodes[0]), 0
    else:
        # Get sample sum
        sample_sum = sum(episodes)
        # Get sample variance
        sample_variance = (sum(np.square(episodes)) - (sample_sum * sample_sum) / runs) / (runs - 1)
        # Get sample mean
        mean = sample_sum / runs
        # Get sample standard deviation
        standard_deviation = math.sqrt(sample_variance)
        # Get the median and inter quartile range
        median, inter_quartile_range = get_quartiles(runs, episodes)
        # Compile mean, standard deviation and sample size to calculate t-test
        main_results = (mean, standard_deviation, runs)
        # Compile other results like median, inter quartile range, max and min
        supporting_results = (median, inter_quartile_range, max(episodes), min(episodes))
        # Calculate the expected difference between the two samples using the t-test
        t_value = calculate_t_value(t_test_values, main_results)
        # Return all results
        return main_results, supporting_results, t_value


# Print out all results of experiment
def print_results(results, failed):
    main_results, supporting_results, t_value = results
    print("")
    print("Mean = %.2f" % main_results[0])
    print("Standard Deviation = %.2f" % main_results[1])
    print("Median = %.1f" % supporting_results[0])
    print("Inter-Quartile Range = %.1f" % supporting_results[1])
    print("Max = %d" % supporting_results[2])
    print("Min = %d" % supporting_results[3])
    print("Runs failed: %d" % len(failed))
    print("Failed runs:", failed)
    print("Difference = %.2f" % t_value)
