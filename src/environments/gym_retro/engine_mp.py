import os
import retro

import torch.multiprocessing as mp

from core.mad_rl import MAD_RL


class Engine:

    def __init__(self):
        pass

    def train_worker(self, config, game, render):
        env = retro.make(game)
        agent = MAD_RL.agent()

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            agent.start_episode(episode)

            step = 0
            while not game_finished:
                for step in range(config["steps_per_episode"]):
                    agent.start_step(step)

                    observation = env.render(mode='rgb_array')
                    action = agent.get_action(observation)

                    next_observation, reward, game_finished, info = env.step(
                        action)

                    if render:
                        env.render()

                    agent.add_experience(
                        observation, reward, action, next_observation, info=info)
                    agent.end_step(step)

                    step = step + 1

                    if game_finished:
                        break

                agent.train()

            agent.end_episode(episode)

    def train(self):

        config = MAD_RL.config()
        game = os.getenv('GAME', "")
        env_render = os.getenv('ENV_RENDER', True)
        number_of_workers = os.getenv('NUMBER_WORKERS', 4)

        processes = []
        for rank in range(0, number_of_workers):
            p = mp.Process(target=self.train_worker, args=(config, game, env_render))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
