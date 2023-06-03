from abc import ABC, abstractmethod


class EnvFunctions(ABC):
    @abstractmethod
    def __init__(self, parameter_settings):
        """Unpack parameters settings"""
        [self.num_q_table, self.num_state, self.num_action,
         self.random_type, self.opposition, self.reward_type] = parameter_settings
        """Define state bounds and constants and initialise environment"""

    def env_functions(self):
        # Returns functions used in environment
        return [self.step_function, self.state_to_bucket, self.action_function,
                self.success_function, self.reward_function()]

    @abstractmethod
    def step_function(self, state, action):
        """Step function for opposition learning"""

    @abstractmethod
    def state_to_bucket(self, obv):
        """Change observations into state buckets"""

    @abstractmethod
    def action_function(self, action):
        """Process and return main and opposite actions"""

    @abstractmethod
    def success_function(self, time_steps, rewards, last_obv):
        """Check for success condition after each episode"""

    @abstractmethod
    def reward_function(self):
        """Returns reward function used by agent"""
