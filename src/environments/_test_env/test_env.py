'''
    This is a Mock Environment only for testing purposes.
    This Mock Environment implements the very mandatory methods that an RL environment should has.
    Usually you will use an Environment like OpenAI Gym which has almost the same main methods.
'''

class Test_Env():

    def __init__(self):
        self.action_space = [1]
        self.next_observation = []
        self.reward = 0
        self.game_finished = False

    def next_step(self, action):
        self.next_observation.append(1)
        if len(self.next_observation) > 100:
            self.game_finished = True
        self.reward = self.reward + 0.01
        return self.next_observation, self.reward, self.game_finished

    def reset(self):
        self.next_observation = []
        self.reward = 0
        self.game_finished = False
    
    def get_observation(self):
        return self.next_observation
