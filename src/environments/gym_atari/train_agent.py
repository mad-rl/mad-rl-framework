import os
import gym

from core.mad_rl import MAD_RL

class Environment:

    def __init__(self):
        pass

    def run(self):

        config = MAD_RL.config()

        GAME = os.getenv('GAME', "")
        ENV_RENDER = os.getenv('ENV_RENDER', True)

        env = gym.make(GAME)
        agent = MAD_RL.agent(action_space=env.action_space)

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

                    if ENV_RENDER:
                        env.render()

                    agent.add_experience(observation, reward, action, next_observation)
                    agent.end_step(step)

                    step = step +1
                    
                    if game_finished:
                        break
                
                agent.train()
            
            agent.end_episode(episode)
