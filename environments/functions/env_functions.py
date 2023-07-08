from abc import ABC, abstractmethod


class EnvFunctions(ABC):
    @abstractmethod
    def __init__(self, parameter_settings):
        """Unpack parameters settings"""
        [self.num_q_table, self.num_state, self.num_action,
         self.random_type, self.opposition, self.reward_type] = parameter_settings
        """Define state bounds and constants"""

    def env_functions(self):
        # Returns functions used in environment
        return [self.step_function, self.state_to_bucket, self.action_function,
                self.success_function, self.reward_function()]

    @abstractmethod
    def step_function(self, obv, action):
        """Step function for opposition learning"""

    @abstractmethod
    def state_to_bucket(self, obv):
        """Change observations into state buckets"""

    @abstractmethod
    def action_function(self, q_action):
        """Process and return opposite q-action, main and opposite actions"""

    @abstractmethod
    def success_function(self, time_steps, rewards, obv):
        """Check for success condition after each episode"""

    @abstractmethod
    def reward_function(self):
        """Returns reward function used by agent"""
