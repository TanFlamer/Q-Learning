import random
import gym.vector
import numpy as np

from code.genetic_algorithm import GeneticAlgorithm
from code.q_learning import QLearning


def reset_data(qLearning, hyperparameters, time_steps, rewards):
    # Clear time steps
    time_steps.clear()
    # Clear rewards
    rewards.clear()
    # Reset agent
    qLearning.reset_agent(hyperparameters)


class ReinforcementLearning:
    def __init__(self):

        # Training settings
        self.runs = None
        self.episodes = None
        self.turns = None

        # Functions
        self.step_function = None
        self.state_to_bucket = None
        self.action_function = None
        self.success_function = None
        self.reward_function = None

        # Gym env and agent
        self.env = None
        self.seed = 0
        self.total_runs = 0
        self.other_settings = None
        self.qLearning_list = []

    def unpack_settings(self, train_settings, env_functions, other_settings):
        # Unpack training settings
        [self.runs, self.episodes, self.turns] = train_settings
        # Unpack functions
        [self.step_function, self.state_to_bucket, self.action_function,
         self.success_function, self.reward_function] = env_functions
        # Unpack other settings
        self.other_settings = other_settings

    def create_env(self, env_id, env_settings):
        # Unpack env settings
        [env_copies, render, self.seed] = env_settings
        # Set seed
        random.seed(self.seed)
        np.random.seed(self.seed)
        # Create env
        self.env = gym.vector.make(env_id, num_envs=env_copies, render_mode="human" if render else None)

    def create_agent(self, parameter_settings):
        # Create copies of Q-Learning agent
        for x in range(self.env.num_envs):
            # Create single Q-Learning agent
            qLearning = QLearning(parameter_settings)
            # Append to Q-Learning list
            self.qLearning_list.append(qLearning)

    def run_experiment(self, hyperparameters, runs, exclude_failure):

        # Reset the environment
        old_obv_list, _ = self.env.reset(options=self.other_settings, seed=self.seed)

        # Results lists
        env_copies = self.env.num_envs
        results = []
        rewards_list = [[] for _ in range(env_copies)]
        time_steps_list = [[] for _ in range(env_copies)]
        reward_total_list = [0 for _ in range(env_copies)]

        # Initialise Q-Learning agents
        self.initialise_agents(hyperparameters, old_obv_list)

        # Run until enough results
        while len(results) < runs and self.total_runs < self.runs:

            # Get action lists
            actions, opposite_actions = self.get_actions()

            # Execute the actions
            obv_list, _, terminations, _, _ = self.env.step(actions)

            # Loop through Q-Learning agents
            for index, qLearning in enumerate(self.qLearning_list):

                # Get main single instance
                obv = obv_list[index]
                action = actions[index]
                terminated = terminations[index]

                # Get other single instance
                opposite_action = opposite_actions[index]
                time_steps = time_steps_list[index]
                rewards = rewards_list[index]

                # Update main action
                state, reward = self.update_table(qLearning, obv, action, terminated)
                reward_total_list[index] += reward

                # Opposition learning
                if opposite_action is not None:
                    # Execute opposite action
                    opposite_obv, opposite_terminated = self.step_function(old_obv_list[index], opposite_action)
                    # Update opposite action
                    self.update_table(qLearning, opposite_obv, opposite_action, opposite_terminated)

                # Save old observations
                old_obv_list = obv_list
                turns = qLearning.turns

                # Termination
                if terminated or turns >= self.turns:

                    # Append time steps and rewards
                    time_steps.append(turns)
                    rewards.append((reward_total_list[index], turns))
                    reward_total_list[index] = 0

                    # Variables
                    success = self.success_function(time_steps, rewards, obv)
                    episodes = qLearning.episodes

                    # Success or failure
                    if success or episodes >= self.episodes:
                        # Add to total runs
                        self.total_runs += 1
                        # Print message
                        status = "succeeded" if success else "failed"
                        print("Agent %s %s in %d episodes for run %d" % (index, status, episodes, self.total_runs))
                        # Append to results
                        if success or not exclude_failure: results.append(qLearning.episodes)
                        # Reset agent
                        reset_data(qLearning, hyperparameters, time_steps, rewards)

                    # Load new episode
                    qLearning.new_episode(state)

                else:
                    # Load new turn
                    qLearning.save_state(state)

        else:
            # Return results and runs
            return results, self.total_runs

    def run_genetic_algorithm(self, tune_setting):
        # Create genetic algorithm agent
        genetic_agent = GeneticAlgorithm(tune_setting, self.run_experiment, self.other_settings)
        # Run genetic algorithm
        return genetic_agent.run_algorithm(self.env.num_envs)

    def initialise_agents(self, hyperparameters, obv):

        # Initialise Q-Learning agents
        for index, qLearning in enumerate(self.qLearning_list):

            # Reset Q-Learning agents
            qLearning.reset_agent(hyperparameters)
            # Get initial state
            state = self.state_to_bucket(obv[index])
            # Initialise new episode
            qLearning.new_episode(state)

    def get_actions(self):

        # Action lists
        actions = []
        opposite_actions = []

        # Loop through Q-Learning agents
        for qLearning in self.qLearning_list:

            # Select Q-tables
            qLearning.select_tables()
            # Select main action
            action = qLearning.select_action()
            # Get main and opposite action
            action, opposite_action = self.action_function(action)

            # Append to action lists
            actions.append(action)
            opposite_actions.append(opposite_action)

        # Return action lists
        return actions, opposite_actions

    def update_table(self, qLearning, obv, action, terminated):
        # Get state
        state = self.state_to_bucket(obv)
        # Get reward
        reward = self.reward_function(obv, terminated, qLearning.turns)
        # Update Q-table
        qLearning.update_table(state, action, reward)
        # Return state and reward
        return state, reward
