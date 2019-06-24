import numpy as np

from .sensor import Sensor

class Interpreter():
    
    def __init__(self, frames=4, width=84, height=84):
        self.width = width
        self.height = height
        self.frames = frames

        self.state = np.zeros([self.frames, self.width, self.height])

    def obs_to_state(self, observation):
        sensor = Sensor(observation,self.width, self.height)
        if len(self.state) == 0:
            for i in range(self.frames):
                self.state[i, :, :] = sensor.data
        else:
            self.state[:self.frames - 1, :, :] = self.state[1:, :, :]
            self.state[self.frames - 1, :, :]  = sensor.data
        return self.state

    def reset(self):
        self.state = np.zeros([self.frames, self.width, self.height])