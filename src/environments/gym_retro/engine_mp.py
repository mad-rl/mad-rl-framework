import os
import retro

import torch.multiprocessing as mp

from core.mad_rl import MAD_RL
from environments.gym_retro.sf2_actor_critic_policy.knowledge import (
    ActorCritic)


class Engine:

    def __init__(self):
        input_frames = 16
        action_space = 49
        self.shared_model = ActorCritic(
            input_frames, num_outputs=action_space)
        self.shared_model.share_memory()

    def train_worker(self, config, game, render):
        env = retro.make(game)
        agent = MAD_RL.agent()
        agent.knowledge.load_shared_model(self.shared_model)

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            agent.start_episode(episode)
            observation = env.render(mode='rgb_array')
            step = 0
            while not game_finished:
                agent.start_step(step)
                action = agent.get_action(observation)
                for step in range(config["steps_per_episode"]):
                    next_observation, reward, game_finished, info = env.step(
                        action)

                    if render:
                        env.render()

                    agent.add_experience(
                        observation, reward, action, next_observation,
                        info=info
                    )
                    agent.end_step(step)
                    observation = next_observation
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
            p = mp.Process(
                target=self.train_worker, args=(config, game, env_render))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
