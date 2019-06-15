'''
    This program is for testing purposes only.
'''

from core.mad_rl import MAD_RL
from test_env import Test_Env

config = MAD_RL.config()
agent = MAD_RL.agent()

env = Test_Env(GAME)

if __name__ == "__main__":

    game_finished = False
    env.reset()

    agent.start_episode(episode)

    step = 0
    while not game_finished:
        for step in range(config.steps_per_episode):
            agent.start_step(step)

            observation = env.get_observation()
            action = agent.get_action(observation)

            next_observation, reward, game_finished = env.next_step(action)

            agent.add_experience(observation, reward, action, next_observation)
            agent.end_step(step)

            step = step +1
            if game_finished:
                break
                
    agent.end_episode(episode)

