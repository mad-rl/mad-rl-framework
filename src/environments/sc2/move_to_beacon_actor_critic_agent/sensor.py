import numpy as np

from PIL import Image


class Sensor():
    def __init__(self, observation, width=84, height=84):
        self.width = width
        self.height = height
        self.data = self.preprocess_obs(observation)

    def preprocess_obs(self, observation):
        image = Image.frombytes(
            mode='RGB',
            size=(observation.minimap.size.x, observation.minimap.size.y),
            data=observation.minimap.data)
        image = image.convert('L')
        image = image.resize((self.width, self.height))
        image_array = np.array(image).astype('float32')
        image_array = image_array * (1.0 / 255.0)

        return image_array


class SC2EnvObservation():
    def __init__(self, observation=None):
        if observation is None:
            self.player = None
            self.units = None
            self.score = None
            self.map = None
            self.minimap = None
        else:
            self.player = observation.observation.observation.player_common
            self.units = observation.observation.observation.raw_data.units
            self.score = observation.observation.observation.score
            self.map = observation.observation.observation.render_data.map
            self.minimap = (
                observation.observation.observation.render_data.minimap)

    def info(self):
        return """--player--\n{}--units--\n{}--score
                  --\n{}--map--\n{}--minimap--\n{}""".format(
                      self.player, self.units, self.score,
                      self.map, self.minimap)

    def own_units(self):
        own_units = []
        for unit in self.units:
            if unit.owner == self.player.player_id:
                own_units.append(unit)
        return own_units
