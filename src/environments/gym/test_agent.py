import os
import gym

from core.mad_rl import MAD_RL

config = MAD_RL.config()

env = gym.make(config['game'])
agent = MAD_RL.agent(action_space=env.action_space)


if __name__ == "__main__":

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

                next_observation, reward, game_finished = env.next_step(action)

                agent.end_step(step)

                step = step +1
                
                if game_finished:
                    break
        
        agent.end_episode(episode)
