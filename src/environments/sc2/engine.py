import os

from .sc2_env import SC2Env
from core.mad_rl import MAD_RL


class Engine:

    def __init__(self):
        pass

    def train(self):

        config = MAD_RL.config()

        env = SC2Env()
        env.start()
        # agent = MAD_RL.agent()

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            # agent.start_episode(episode)

            step = 0
            while not game_finished:
                for step in range(config["steps_per_episode"]):
                    # agent.start_step(step)

                    observation = env.get_observation()

                    print(observation)
            #        action = agent.get_action(observation)

                    next_observation, reward, game_finished = env.step()

            #        agent.add_experience( observation, reward, action, next_observation)
            #       agent.end_step(step)

                    step = step + 1

                    if game_finished:
                        break

            #    agent.train()

            # agent.end_episode(episode)
