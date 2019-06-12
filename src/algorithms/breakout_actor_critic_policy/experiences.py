import numpy as np
from agent_base.experiences_base import ExperiencesBase

class Experiences(ExperiencesBase):

    def __init__(self, size=128):
        ExperiencesBase.__init__(self)

    def add(self, state, reward, action, next_state):
        self.experiences.append(
            (state.tolist(), reward, action, next_state.tolist())
        )

    def get(self, batch_size=None):
        if not batch_size:
            return np.array(self.experiences)
        else:
            return np.array(self.experiences[batch_size])

    def reset(self):
        self.experiences = []
