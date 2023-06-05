class ReinforcementLearning:
    def __init__(self, env, qLearning, train_settings, functions):
        # Environment
        self.env = env
        # Q-Learning agent
        self.qLearning = qLearning
        # Unpack settings
        [self.runs, self.episodes, self.turns, self.exclude_failure] = train_settings
        # Unpack functions
        [self.step_function, self.state_to_bucket, self.action_function,
         self.success_function, self.reward_function] = functions

    def train_agent(self, hyperparameters):

        # Results list
        results = []
        # Reset Q-Learning agent
        self.qLearning.reset_agent(hyperparameters)

        # Run until enough results
        while len(results) < self.runs:

            # Start new run
            self.qLearning.new_run()
            # Save time steps
            time_steps = [0]

            # Run until run completes
            for episode in range(self.episodes):

                # Reset the environment
                obv, _ = self.env.reset()
                # Get state
                state = self.state_to_bucket(obv)
                # New Q-Table
                self.qLearning.new_episode(state)

                # Run one episode
                time_step, rewards, last_obv = self.single_episode(obv)
                # Append time step cumulatively
                time_steps.append(time_step + time_steps[-1])

                # Check success condition
                if self.success_function(time_steps, rewards, last_obv):
                    # Record result for success
                    results.append(episode + 1)
                    break
            else:
                # Record result for failure
                if not self.exclude_failure: results.append(self.episodes)

        else:
            # Return results
            return results

    def single_episode(self, initial_obv):

        # Save previous state
        old_obv = initial_obv
        # Rewards list
        rewards = []

        # Run until episode completes
        for turn in range(self.turns):

            # Select Q-tables
            self.qLearning.select_tables()
            # Select main action
            action = self.qLearning.select_action()
            # Process main and opposite action
            action, opposite_action = self.action_function(action)

            # Execute the action
            obv, _, terminated, _, _ = self.env.step(action)
            # Get state
            state = self.state_to_bucket(obv)
            # Get reward
            reward = self.reward_function(obv, terminated, turn)
            # Update Q-table
            self.qLearning.update_table(state, action, reward)

            # Opposition learning
            if opposite_action is not None:
                # Execute opposite action
                opposite_obv, opposite_terminated = self.step_function(old_obv, opposite_action)
                # Get opposite state
                opposite_state = self.state_to_bucket(opposite_obv)
                # Get opposite reward
                opposite_reward = self.reward_function(opposite_obv, opposite_terminated, turn)
                # Update opposite Q-table
                self.qLearning.update_table(opposite_state, opposite_action, opposite_reward)

            # Save old state
            self.qLearning.save_state(state)
            old_obv = obv

            # Append reward
            rewards.append(reward)

            # Episode termination
            if terminated: return turn + 1, rewards, obv

        else:
            # Episode timeout
            return self.turns, rewards, None
