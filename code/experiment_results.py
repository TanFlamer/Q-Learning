import math
import numpy as np
import scipy


class Results:
    def __init__(self, t_test_values, results):
        # Unpack t-test values
        [self.confidence_level, self.first_mean, self.first_std, self.first_size] = t_test_values
        # Unpack results
        self.results = results
        # Get failed length
        self.failed = self.results.pop() - len(self.results)

    def print_results(self, exp_results):
        # Get statistics
        [mean, std, median, inter_quartile_range,
         max_val, min_val, difference, failed] = exp_results

        # Print statistics
        print("\nResults =", self.results)
        print("Mean = %.2f" % mean)
        print("Standard Deviation = %.2f" % std)
        print("Median = %.1f" % median)
        print("Inter-Quartile Range = %.1f" % inter_quartile_range)
        print("Max = %d" % max_val)
        print("Min = %d" % min_val)
        print("Failed runs = %d" % failed)
        print("Difference = %.2f" % difference)

    def get_statistics(self):
        # Sort results
        self.results.sort()

        # Get mean, STD and difference
        mean = np.mean(self.results)
        std = np.std(self.results, ddof=1)
        difference = self.calculate_difference(mean, std)

        # Get quartiles
        length = len(self.results)
        half, offset = length // 2, length % 2
        [min_val, median, max_val] = np.quantile(self.results, [0, 0.5, 1])
        first_q, third_q = np.median(self.results[:half]), np.median(self.results[half + offset:])

        # Compile and return results
        exp_results = [mean, std, median, third_q - first_q, max_val, min_val, difference, self.failed]
        self.print_results(exp_results)
        return exp_results

    def calculate_difference(self, second_mean, second_std):
        # Get second sample size
        second_size = len(self.results)
        # Get pooled standard deviation of both samples
        pooled_std = self.get_pooled_std(second_std, second_size)
        # Calculate noise of t-test
        noise = pooled_std * math.sqrt(1 / self.first_size + 1 / second_size)
        # Get critical value from confidence level and degrees of freedom
        critical_value = scipy.stats.t.ppf(self.confidence_level, self.first_size + second_size - 2)
        # Calculate the expected difference between the two samples
        difference = (self.first_mean - second_mean) - (critical_value * noise)
        # Return the expected difference or 0 if t-test fails
        return max(difference, 0)

    def get_pooled_std(self, second_std, second_size):
        # Get sum of squares
        def sum_of_square(std, size): return (std * std) * (size - 1)
        # Get sum of squares of samples
        first_data, second_data = sum_of_square(self.first_std, self.first_size), sum_of_square(second_std, second_size)
        # Get pooled variance of both samples
        pooled_variance = (first_data + second_data) / (self.first_size + second_size - 2)
        # Get pooled standard deviation of both samples
        return math.sqrt(pooled_variance)
