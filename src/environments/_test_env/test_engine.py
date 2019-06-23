'''
    This training loop is for testing purposes only.
    You can see real rraining loop implementations within other environments.
    However this is 100% valid training loop and you can check how most of the agents and environments within MAD_RL_ uses a very similar training loop
'''

from core.mad_rl import MAD_RL
from environments._test_env.test_env import Test_Env

class Engine:

    def __init__(self):
        pass

    def train(self):
        config = MAD_RL.config()
        env = Test_Env()

        agent = MAD_RL.agent(action_space=env.action_space)

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            agent.start_episode(episode)

            step = 0
            while not game_finished:
                for step in range(config["steps_per_episode"]):
                    agent.start_step(step)

                    observation = env.get_observation()
                    action = agent.get_action(observation)

                    next_observation, reward, game_finished = env.next_step(action)

                    agent.add_experience(observation, reward, action, next_observation)
                    agent.end_step(step)

                    step = step +1
                    
                    if game_finished:
                        break
                
                agent.train()
            
            agent.end_episode(episode)

    def test(self):
        config = MAD_RL.config()
        env = Test_Env()

        agent = MAD_RL.agent(action_space=env.action_space)

        for episode in range(config["episodes"]):
            game_finished = False
            env.reset()

            agent.start_episode(episode)

            step = 0
            while not game_finished:
                agent.start_step(step)

                observation = env.get_observation()
                action = agent.get_action(observation)

                next_observation, reward, game_finished = env.next_step(action)

                agent.end_step(step)

                step = step +1
                
                if game_finished:
                    break

            agent.end_episode(episode)
