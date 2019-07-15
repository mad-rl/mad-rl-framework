from .sensor import Sensor


class Interpreter():
    def __init__(self, frames=4, width=84, height=84):
        self.width = width
        self.height = height
        self.frames = frames
        self.state = [self.frames, self.width, self.height]

    def obs_to_state(self, observation):
        sensor = Sensor(observation, self.width, self.height)
        return sensor.data

    def reset(self):
        self.state = [self.frames, self.width, self.height]
