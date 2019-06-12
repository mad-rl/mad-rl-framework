
class AgentBase:

    def __init__(self, knowledge, interpreter, actuator, experiences):
        self.knowledge = knowledge
        self.interpreter = interpreter
        self.actuator = actuator
        self.experiences = experiences

    def get_action(self, observation):
        return self.actuator.model_to_env(self.knowledge.get_action(observation))

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