from agent.experiences_base import ExperiencesBase

class Experiences(ExperiencesBase):

    def __init__(self):
        ExperiencesBase.__init__(self)

    def add(self, observation, reward, action, next_observation):
        pass

    def get(self):
        pass