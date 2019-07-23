import os
from .sc2_env import SC2Env

import torch.multiprocessing as mp

from core.mad_rl import MAD_RL
from environments.sc2.move_to_beacon_actor_critic_agent.knowledge import (
    ActorCritic)


class Engine:

    def __init__(self):
        input_frames = 1
        action_space = 48 * 48
        self.shared_model = ActorCritic(
            input_frames, num_outputs=action_space)
        self.shared_model.double()
        self.shared_model.share_memory()

    def train_worker(self, config, rank, game, render):
        env = SC2Env(conn_port=(5000 + rank))
        env.start()
        agent = MAD_RL.agent()

        agent.knowledge.load_shared_model(self.shared_model)

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            agent.start_episode(episode)
            observation = env.get_observation()

            step = 0
            while not game_finished:
                action = agent.get_action(observation)

                for step in range(config["steps_per_episode"]):
                    agent.start_step(step)

                    next_observation, reward, game_finished = env.step(action)

                    agent.add_experience(
                        observation, reward, action, next_observation)
                    agent.end_step(step)

                    # env.render()

                    observation = next_observation
                    step = step + 1

                    if game_finished:
                        break

                agent.train()

            agent.end_episode(episode)

    def train(self):

        config = MAD_RL.config()
        game = os.getenv('GAME', "")
        env_render = os.getenv('ENV_RENDER', False)
        number_of_workers = os.getenv('NUMBER_WORKERS', 4)

        processes = []
        for rank in range(0, number_of_workers):
            p = mp.Process(
                target=self.train_worker,
                args=(config, rank, game, env_render))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
