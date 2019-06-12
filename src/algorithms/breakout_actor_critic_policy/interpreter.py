import numpy as np

from agent_base.interpreter_base import InterpreterBase
from sensor import Sensor
from PIL import Image

class Interpreter(InterpreterBase):
    
    def __init__(self, frames=4, width=84, height=84):
        InterpreterBase.__init__(self)
        self.width = width
        self.height = height
        self.frames = frames

        self.data = np.zeros([self.frames, self.width, self.height])

    def obs_to_state(self, obs):
        if len(self.data) == 0:
            for i in range(4):
                self.data[i, :, :] = self.preprocess_obs(obs)
        else:
            self.data[:3, :, :] = self.data[1:, :, :]
            self.data[3, :, :]  = self.preprocess_obs(obs)

        return self.data

    def preprocess_obs(self, X):
        x = Image.fromarray(X).convert('L')
        x = x.resize((self.width, self.height))
        x = np.array(x).astype('float32')
        x = x * (1.0 / 255.0)

        return x

    def reset(self):
        self.data = np.zeros([self.frames, self.width, self.height])