from agent_base.agent_base import AgentBase
from knowledge import Knowledge
from interpreter import Interpreter
from actuator import Actuator
from experiences import Experiences

class Agent(AgentBase):

    def __init__(self, action_space):
        AgentBase.__init__(self, Knowledge(action_space),Interpreter(),Actuator(),Experiences())

    def get_action(self, observation):
        return [1]

    def add_experience(self, observation, reward, action, next_observation, info=None):
        self.experiences.add(observation, reward, action, next_observation)
        pass

    def start_step(self, current_step):
        pass

    def end_step(self, current_step):
        pass

    def start_episode(self, current_episode):
        pass

    def end_episode(self, current_episode):
        pass