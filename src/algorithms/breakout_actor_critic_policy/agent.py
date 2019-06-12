import numpy as np

from agent_base.agent_base import AgentBase
from knowledge import Knowledge
from interpreter import Interpreter
from actuator import Actuator
from experiences import Experiences

class Agent(AgentBase):

    def __init__(self, action_space):
        AgentBase.__init__(self, Knowledge(action_space),Interpreter(),Actuator(),Experiences())
        self.rewards = []

    def get_action(self, state):
        action = self.actuator.model_to_env(
            self.knowledge.get_action(state)
        )
        return action

    def add_experience(self, state, reward, action, next_state, info=None):
        action = self.actuator.env_to_model(action)
        self.experiences.add(state, reward, action, next_state)
        self.rewards.append(reward)

    def start_step(self, current_step):
        pass

    def end_step(self, current_step):
        pass

    def start_episode(self, current_episode):
        self.interpreter.reset()

    def end_episode(self, current_episode):
        print("Episode rewards:")
        print(np.sum(np.array(self.rewards)))
        self.rewards = []

    def train(self):
        self.knowledge.train(self.experiences.get())
        self.experiences.reset()
