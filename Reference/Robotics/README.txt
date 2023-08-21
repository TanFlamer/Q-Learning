This README explains how to run the experiments
effectively. Users must first copy all the python
files provided into a new project.

To be able to run the files in the folder, some
python packages need to be installed first. These
packages are:
    1. numpy
    2. gym
    3. scipy
    4. math

5 files are included in the folder which are:
    1. acrobot_settings.py
    2. acrobot_template.py
    3. cartpole_settings.py
    4. cartpole_template.py
    5. results_processing.py

There are three types of files in the folder:
    1. template files
    2. results file
    3. setting files

Template files and results file are not meant to be modified and
should be treated as a blackbox. Template files include all the
code needed to run the experiments while results file process
all the data generated in the experiment to produce results to
be viewed by the user. Template files include acrobot_template.py
and cartpole_template.py. Result file include result_processing.py.

Setting files are the files which are meant to be modified
to change the experiment settings to get different results.
After all modifications are done, users can run the current
file to get results. Setting files include acrobot_settings.py
and cartpole_settings.py.

Setting files can be modified to include different improvements to
the existing Q-learning algorithm. Some improvements such as
granularity, discount factor and random initialisation of initial
Q-table values have a range of possible values. To facilitate
easier testing and comparison, fixed values have been chosen so
that the improvement becomes a binary choice. Either we use the
default value or we use the fixed value chosen. The exception to
this rule is the Q-tables number which can range from 1 to 5. The
default values are listed inside the settings file but will also
be shown below. The default values are:
    1. Q-tables number - 1
    2. Granularity (Cartpole) - (1, 1, 6, 3)
    3. Granularity (Acrobot) - (1, 1, 1, 1, 10, 10)
    4. Opposition Learning - False
    5. Initial Q-table values - 0
    6. Discount factor - True
    7. Number of actions (Acrobot) - 3

Setting files can also be used to modify the reward function of
the Q-learning algorithm. Users just have to replace the function
in the return statement of the reward function and supply the
reward function with the required parameters.

Setting files can also be used to change the calculation for the
expected difference between two samples. The default confidence
level of the t-test is 0.99 but users can freely change this value.

Users are required to supply the t-test with data about the first
sample to be compared such as mean, standard deviation and sample size.
The default data used are the results for Cartpole and Acrobot with
no improvements to the algorithm and the base reward function.

Default sample data for Cartpole:
    Mean - 257.27
    Standard Deviation - 14.94
    Sample Size - 30

Default sample data for Acrobot:
    Mean - 293.87
    Standard Deviation - 36.64
    Sample Size - 30
