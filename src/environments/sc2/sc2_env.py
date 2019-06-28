from s2clientprotocol import sc2api_pb2 as s2api
from s2clientprotocol import common_pb2 as s2common
from websocket import create_connection


class SC2Env():

    def __init__(self, conn_host="127.0.0.1", conn_port=5000, conn_root_api="sc2api"):
        self._ws = create_connection("ws://{host}:{port}/{root_api}".format(
            host=conn_host, port=conn_port, root_api=conn_root_api))

        self.action_space = [1]
        self.next_observation = []
        self.reward = 0
        self.game_finished = False

    def __request_proto__(self, service, protoRequest, protoResponse):
        # print('__request_proto__', service, protoObject)
        self._ws.send(s2api.Request(
            **{service: protoRequest}).SerializeToString())
        result_raw = self._ws.recv()
        res = s2api.Response(**{service: protoResponse})
        res.ParseFromString(result_raw)
        return res

    def start(self, local_map='mini_games/MoveToBeacon.SC2Map', race=s2common.Race.Value('Terran')):
        print(local_map, race)
        self.__request_proto__(
            "ping", s2api.RequestPing(), s2api.ResponsePing())

        createGame = s2api.RequestCreateGame(local_map={'map_path': local_map}, player_setup=[
                                             {'type': s2api.PlayerType.Value('Participant'), 'race': race}], realtime=False)
        self.__request_proto__("create_game", createGame,
                               s2api.ResponseCreateGame())

        joinGame = s2api.RequestJoinGame(
            race=race, options={'raw': True, 'score': True})
        self.__request_proto__("join_game", joinGame, s2api.ResponseJoinGame())

    def step(self, action):
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
        return []
