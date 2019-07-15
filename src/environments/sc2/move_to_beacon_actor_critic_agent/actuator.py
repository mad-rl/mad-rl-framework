import numpy as np


class Actuator():
    def __init__(self):
        self.custom_width = 48
        self.custom_height = 48
        self.last_action = 0

    def agent_to_env(self, agent_action):
        self.last_action = agent_action
        y = min(int(np.ceil(agent_action / self.custom_height)),
                self.custom_height - 1)
        x = int(agent_action % self.custom_width)
        coordinates = {'x': x, 'y': y}

        return {'ability_id': 16, 'target_world_space_pos': coordinates}

    def env_to_agent(self, env_action):
        return self.last_action
