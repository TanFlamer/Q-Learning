This README explains how to run the GUI correctly.
Users must first copy all the python files
provided into a new python project.

To be able to run the GUI, some python packages
need to be installed first. These packages are:
    1. tkinter
    2. scipy
    3. numpy

There are 3 distinct files provided: main.py and
2 packages named code and gui. The GUI is run by
running the code inside main.py.

The first package is named code. The files within
control the entire experiment process.
- brick_breaker.py holds the Brick Breaker game
  and is the environment used for the experiments.
- bricks.py controls the generation of bricks used
  by the Brick Breaker game.
- commands.py holds the functions used by the GUI.
- experiment_results.py compiles and displays the
  results for the experiments.
- genetic_algorithm.py runs Genetic Algorithm and
  is used for hyperparameter tuning.
- q_learning.py controls the Q-Learning agent which
  learns to play the Brick Breaker game.

The second package is named gui. The files within
control the GUI of the project. More information
about the GUI can be found in the report.
- initial_gui.py controls the GUI to get user
  input for the experiments.
- results.gui.py controls the GUI to show the
  results after the experiments.
- widgets.py holds all the widgets used by the GUI.

Default sample data for the experiments:
    Confidence - 0.990
    Mean - 45.63
    STD - 1.40
    Old Runs - 30
