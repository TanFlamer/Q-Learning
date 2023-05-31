from .brick_breaker import Game
from .genetic_algorithm import GeneticAlgorithm
from .q_learning import QLearning
from .experiment_results import Results
from .bricks import get_bricks


def run_genetic_algorithm(root, initial_settings, tuning_settings, dimensions, display_tune_results):
    # Split settings
    brick_settings, total_settings = split_settings_list(initial_settings, 4)
    other_settings = [dimensions, get_bricks(brick_settings), 1, False]
    fitness_settings = [root, total_settings, other_settings]
    # Run Genetic Algorithm
    best_chromosomes = GeneticAlgorithm(tuning_settings, run_brick_breaker, fitness_settings).run_algorithm()
    # Display results
    display_tune_results(root, initial_settings, tuning_settings, best_chromosomes)


def run_experiment(root, initial_settings, experiment_settings, dimensions, display_exp_results):
    # Split settings
    brick_settings, total_settings = split_settings_list(initial_settings, 4)
    hyper_parameters, result_settings = split_settings_list(experiment_settings, 9)
    other_settings = [dimensions, get_bricks(brick_settings), result_settings[0], True]
    # Run Brick Breaker
    results = run_brick_breaker(root, total_settings, other_settings, hyper_parameters)
    # Display results
    exp_results = Results(result_settings[1:], results).get_statistics()
    display_exp_results(root, initial_settings, experiment_settings, exp_results)


def run_brick_breaker(root, total_settings, other_settings, hyper_parameters):
    # Split total settings
    game_settings, parameter_settings = split_settings_list(total_settings, 4)
    # Load Q-Learning
    qLearning = QLearning(parameter_settings, hyper_parameters, other_settings[0])
    # Save results
    results = []
    # Run game
    game = Game(root, game_settings, other_settings, qLearning, results)
    game.pack(fill='both', expand=1)
    game.mainloop()
    # Return results
    return results


def split_settings_list(settings_list, index):
    # Split settings list in 2
    return settings_list[:index], settings_list[index:]
