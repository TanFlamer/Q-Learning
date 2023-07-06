import math
import numpy as np
import scipy


class Results:
    def __init__(self, result_settings, results, total_runs):
        # Unpack t-test values
        [self.confidence_level, self.first_mean, self.first_std, self.first_size] = result_settings
        # Unpack results
        self.results = results
        # Get failed length
        self.failed = total_runs - len(self.results)

    def get_statistics(self):
        # Result labels
        exp_labels = ["Mean", "Standard Deviation", "Runs", "Max", "Min", "Median",
                      "Inter-Quartile Range", "Difference", "Failed Runs"]

        # Get results length
        length = len(self.results)

        # If no success
        if length == 0:
            # Return all 0s
            exp_results = [0, 0, length, 0, 0, 0, 0, 0, self.failed]

        # If one success
        elif length == 1:
            # Get only result
            result = self.results[0]
            # Return result
            exp_results = [result, 0, length, result, result, result, 0, 0, self.failed]

        # If more success
        else:
            # Sort results
            self.results.sort()

            # Get mean, STD and difference
            mean = np.mean(self.results)
            std = np.std(self.results, ddof=1)
            difference = self.calculate_difference(mean, std)

            # Get quartiles
            half, offset = length // 2, length % 2
            [min_val, median, max_val] = np.quantile(self.results, [0, 0.5, 1])
            first_q, third_q = np.median(self.results[:half]), np.median(self.results[half + offset:])

            # Return result
            exp_results = [mean, std, length, max_val, min_val, median, third_q - first_q, difference, self.failed]

        # Print results
        self.print_results(exp_results)

        # Return results
        return [("Experiment Results", list(zip(exp_labels, exp_results)))]

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

    def print_results(self, exp_results):
        # Get statistics
        [mean, std, runs, max_val, min_val, median,
         inter_quartile_range, difference, failed] = exp_results

        # Print statistics
        print("\nResults =", self.results)
        print("Mean = %.2f" % mean)
        print("Standard Deviation = %.2f" % std)
        print("Runs = %d" % runs)
        print("Inter-Quartile Range = %.1f" % inter_quartile_range)
        print("Max = %d" % max_val)
        print("Min = %d" % min_val)
        print("Median = %.1f" % median)
        print("Difference = %.2f" % difference)
        print("Failed runs = %d" % failed)
