class ReinforcementLearning:
    def __init__(self, env, qLearning, env_settings, train_settings):
        # Q-Learning agent and results
        self.env = env
        self.qLearning = qLearning
        self.results = []

        # Unpack settings and functions
        [self.num_q_table, self.num_state, self.num_action,
         self.random_type, self.opposition, self.exclude_failure] = env_settings
        [self.runs, self.episodes, self.turns] = train_settings

        # Pack settings
        self.buckets = (self.num_state, self.num_action)
        self.table_settings = [self.num_q_table, self.random_type, self.buckets]

    def train_agent(self):
        # Run until enough results
        while len(self.results) < self.runs:

            # Save time steps
            time_steps = [0]
            # Start new run
            self.qLearning.new_run(self.table_settings)

            # Run until run completes
            for episode in range(self.episodes):

                # Reset the environment
                obv, _ = self.env.reset()
                # Get state
                state = self.env.state_to_bucket(obv, self.buckets)
                # New Q-Table
                self.qLearning.new_episode(state)
                # New episode
                last_obv = self.single_episode(obv, time_steps)

                # Check success condition
                if self.env.success_function(last_obv, time_steps):
                    # Record result for success
                    self.results.append(episode + 1)
                    break
            else:
                # Record result for failure
                if not self.exclude_failure: self.results.append(self.episodes)

        else:
            # Return results
            return self.results

    def single_episode(self, initial_obv, time_steps):

        # Save previous state
        old_obv = initial_obv
        # Save last state
        obv = None

        # Run until episode completes
        for turn in range(self.turns):

            # Render environment
            self.env.render()
            # Select Q-tables
            self.qLearning.select_tables()

            # Select main action
            action = self.qLearning.select_action(self.num_action)
            # Process main and opposite action
            action, opposite_action = self.env.action_function(action)

            # Execute the action
            obv, _, terminated, _, _ = self.env.step(action)
            # Get state
            state = self.env.state_to_bucket(obv, self.buckets)
            # Get reward
            reward = self.env.reward_function(obv, terminated, turn)
            # Update Q-table
            self.qLearning.update_table(state, action, reward)

            # Opposition learning
            if self.opposition and opposite_action is not None:
                # Execute opposite action
                opposite_obv, opposite_terminated = self.env.step_function(old_obv, opposite_action)
                # Get opposite state
                opposite_state = self.env.state_to_bucket(opposite_obv, self.buckets)
                # Get opposite reward
                opposite_reward = self.env.reward_function(opposite_obv, opposite_terminated, turn)
                # Update opposite Q-table
                self.qLearning.update_table(opposite_state, opposite_action, opposite_reward)

            # Save old state
            self.qLearning.save_state(obv)
            old_obv = obv

            # Termination
            if terminated:
                # Record time steps to termination cumulatively
                time_steps.append((turn + 1) + time_steps[-1])
                break
        else:
            # Record time steps to termination cumulatively
            time_steps.append(self.turns + time_steps[-1])

        # Return last obv
        return obv
