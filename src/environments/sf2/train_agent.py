import os

import retro

from core.mad_rl import MAD_RL


class Environment:

    def __init__(self):
        pass

    def run(self):
        action_space = 49
        config = MAD_RL.config()

        game = os.getenv('GAME', "")
        env_render = os.getenv('ENV_RENDER', True)

        env = retro.make(game)
        agent = MAD_RL.agent(action_space=action_space)

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

                    next_observation, reward, game_finished, _info = env.step(action)

                    if env_render:
                        env.render()

                    agent.add_experience(observation, reward, action, next_observation, info=_info)
                    agent.end_step(step)

                    step = step +1
                    
                    if game_finished:
                        break
                
                agent.train()
            
            agent.end_episode(episode)
