from core.mad_rl import MAD_RL
from PIL import Image
from websocket import create_connection
from s2clientprotocol import sc2api_pb2 as s2api
from s2clientprotocol import common_pb2 as s2common
from s2clientprotocol import raw_pb2 as s2raw


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


class SC2Env():
    def __init__(self, conn_host="127.0.0.1", conn_port=5000,
                 conn_root_api="sc2api"):
        self._ws = create_connection("ws://{host}:{port}/{root_api}".format(
            host=conn_host, port=conn_port, root_api=conn_root_api))

        self.action_space = [1]
        self.next_observation = []
        self.reward = 0
        self.game_finished = False

        self.last_observation = SC2EnvObservation()

    def __request_proto__(self, service, protoRequest, protoResponse):
        self._ws.send(s2api.Request(
            **{service: protoRequest}).SerializeToString())
        result_raw = self._ws.recv()
        res = s2api.Response(**{service: protoResponse})
        res.ParseFromString(result_raw)
        MAD_RL.debug(res)
        return res

    def __call_action__(self, ability_id, unit_tags, target_world_space_pos):
        actionRawUnitCommand = s2raw.ActionRawUnitCommand(
            ability_id=ability_id,
            unit_tags=unit_tags,
            queue_command=True,
            target_world_space_pos=target_world_space_pos
        )
        actionRaw = s2raw.ActionRaw(unit_command=actionRawUnitCommand)
        self.__request_proto__(
            "action",
            s2api.RequestAction(actions=[s2api.Action(action_raw=actionRaw)]),
            s2api.ResponseAction()
        )

    def __call_step__(self):
        self.__request_proto__(
            "step",
            s2api.RequestStep(),
            s2api.ResponseStep()
        )

    def __call_observation__(self):
        observation = self.__request_proto__(
            "observation",
            s2api.RequestObservation(),
            s2api.ResponseObservation()
        )

        return observation

    def __call_restart_game__(self):
        self.__request_proto__(
            "restart_game",
            s2api.RequestRestartGame(),
            s2api.ResponseRestartGame()
        )

    def start(self, local_map='MoveToBeacon.SC2Map',
              race=s2common.Race.Value('Terran')):
        print(local_map, race)
        self.__request_proto__(
            "ping",
            s2api.RequestPing(),
            s2api.ResponsePing()
        )

        # CREATE GAME
        createGame = s2api.RequestCreateGame(
            local_map={'map_path': local_map},
            player_setup=[{'type': s2api.PlayerType.Value('Participant'),
                           'race': race}],
            realtime=False)
        self.__request_proto__(
            "create_game",
            createGame,
            s2api.ResponseCreateGame()
        )

        # JOIN GAME
        camSetup = s2api.SpatialCameraSetup(
            resolution={'x': 640, 'y': 480},
            minimap_resolution={'x': 640, 'y': 480}
        )
        joinGame = s2api.RequestJoinGame(
            race=race,
            options={'raw': True, 'score': True, 'render': camSetup}
        )
        self.__request_proto__(
            "join_game",
            joinGame,
            s2api.ResponseJoinGame()
        )

        self.last_observation = SC2EnvObservation(self.__call_observation__())

    def step(self, action):
        unit_tags = self.last_observation.own_units()[0].tag
        self.__call_action__(
            action['ability_id'],
            [unit_tags],
            action['target_world_space_pos'])

        self.__call_step__()

        observation = self.__call_observation__()
        self.game_finished = observation.status == 5
        self.save_observation(observation)

        observation = SC2EnvObservation(observation)
        self.next_observation.append(observation)
        self.last_observation = observation
        self.reward += observation.score.score

        return self.last_observation, self.reward, self.game_finished

    def reset(self):
        self.next_observation = []
        self.reward = 0
        self.game_finished = False

        self.__call_restart_game__()

    def get_observation(self):
        return SC2EnvObservation(self.__call_observation__())

    def render(self):
        observation = self.last_observation

        img = Image.frombytes(
            mode='RGB',
            size=(observation.map.size.x, observation.map.size.y),
            data=observation.map.data)
        img.save("./src/environments/sc2/renders/observation_map_data.png")

        img = Image.frombytes(
            mode='RGB',
            size=(observation.minimap.size.x, observation.minimap.size.y),
            data=observation.minimap.data)
        img.save("./src/environments/sc2/renders/observation_minimap_data.png")

        file1 = open("./src/environments/sc2/renders/observation.info", "w")
        observation.map.data = b''
        observation.minimap.data = b''
        file1.write(observation.info())
        file1.close()

    def save_observation(self, observation):
        file1 = open("observation.json", "w")
        file1.write(str(observation))
        file1.close()
