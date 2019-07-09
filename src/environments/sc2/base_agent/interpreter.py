from .sensor import Sensor


class Interpreter():

    def __init__(self, frames=4, width=84, height=84):
        self.width = width
        self.height = height
        self.frames = frames

        self.state = [self.frames, self.width, self.height]

    def obs_to_state(self, observation):
        sensor = Sensor(observation, self.width, self.height)
        if len(self.state) == 0:
            for i in range(4):
                self.state.append(sensor.data)
        else:
            self.state[:-1].append(sensor.data)
        return self.state

    def reset(self):
        self.state = [self.frames, self.width, self.height]
