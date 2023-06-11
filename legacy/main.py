from legacy.code import run_experiment, run_genetic_algorithm
from legacy.gui.initial_gui import run_gui
from legacy.gui import display_tune_results, display_exp_results

# Run the GUI
run_gui(run_experiment, run_genetic_algorithm, display_tune_results, display_exp_results)
