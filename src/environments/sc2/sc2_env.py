from PIL import Image
from websocket import create_connection
from s2clientprotocol import sc2api_pb2 as s2api
from s2clientprotocol import common_pb2 as s2common
from s2clientprotocol import raw_pb2 as s2raw

from .base_agent.sensor import SC2EnvObservation


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
        self.save_observation(observation)

        observation = SC2EnvObservation(observation)
        self.next_observation.append(observation)
        self.last_observation = observation
        self.reward += observation.score.score

        if len(self.next_observation) > 10:
            self.game_finished = True

        return self.last_observation, self.reward, self.game_finished

    def reset(self):
        self.next_observation = []
        self.reward = 0
        self.game_finished = False

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
