'''
    This agent is a base agent that works under the architecture defined in the documentation.
    We are using this base agent to implement a lot of different RL algorithms. 
    We will maintain updated this base agent with the goal of keeping the balance between flexibility and comfortability.
'''

from .knowledge import Knowledge
from .interpreter import Interpreter
from .actuator import Actuator
from .experiences import Experiences

class Agent():

    def __init__(self, action_space):
        self.knowledge = Knowledge(action_space)
        self.interpreter = Interpreter()
        self.actuator = Actuator()
        self.experiences = Experiences()

    def get_action(self, observation):
        state = self.interpreter.obs_to_state(observation)
        agent_action = self.knowledge.get_action( state )
        return self.actuator.agent_to_env( agent_action )

    def add_experience(self, observation, reward, env_action, next_observation):
        agent_action = self.actuator.env_to_agent(env_action)
        state = self.interpreter.obs_to_state(observation)
        next_state = self.interpreter.obs_to_state(next_observation)
        self.experiences.add(state, reward, agent_action, next_state)

    def start_step(self, current_step):
        pass

    def end_step(self, current_step):
        pass

    def start_episode(self, current_episode):
        print('episode', current_episode)
        pass

    def end_episode(self, current_episode):
        pass
    
    def train(self):
        self.knowledge.train(self.experiences.get())
