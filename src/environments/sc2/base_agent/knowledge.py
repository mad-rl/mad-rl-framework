import random

class Knowledge():
    
    def __init__(self, action_space):
        self.action_space = action_space

    def get_action(self, state):
        action = [random.random()*640, random.random()*480]
        return action

    def train(self, experiences):
        pass