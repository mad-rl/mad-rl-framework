import os
# import retro
import gym

RECORD_REPLY = bool(os.getenv('RECORD_REPLY', False))
EPISODES = int(os.getenv('EPISODES', 10))
STEPS_PER_EPISODE = int(os.getenv('STEPS_PER_EPISODE', 100))
# GAME = int(os.getenv('GAME', 'StreetFighterIISpecialChampionEdition-Genesis'))
GAME = os.getenv('GAME', 'BreakoutDeterministic-v4')
ENV_RENDER = os.getenv('ENV_RENDER', True)

AGENT_MODULE = os.getenv('AGENT_MODULE', 'algorithms._new_template.new_agent')
AGENT_CLASS = os.getenv('AGENT_CLASS', 'Agent')

def agent_class(module, class_name):
    sf_agent_mod = __import__(module, fromlist=["*"])
    sf_agent_class = getattr(sf_agent_mod, class_name)
    return sf_agent_class

# env = retro.make(game=GAME)
env = gym.make(GAME)

if RECORD_REPLY is True:
    env.auto_record(path='./reply/')

if __name__ == "__main__":

    sf_agent = agent_class(AGENT_MODULE, AGENT_CLASS)(env.action_space)

    for episode in range(EPISODES):
        game_finished = False
        env.reset()
        # Get initial observation (first state)
        _obs = env.render(mode='rgb_array')
        sf_agent.start_episode(episode)
        state = sf_agent.interpreter.obs_to_state(_obs)

        done = False
        step = 0
        while not done:
            for step in range(STEPS_PER_EPISODE):

                sf_agent.start_step(step)

                action = sf_agent.get_action(state)

                _next_obs, _rew, done, _info = env.step(action)
                next_state = sf_agent.interpreter.obs_to_state(_next_obs)

                sf_agent.add_experience(state, _rew, action, next_state, info=_info)

                state = next_state

                if ENV_RENDER:
                    env.render()

                sf_agent.end_step(step)
                step = step +1

                if done:
                    break

            sf_agent.train()

        sf_agent.end_episode(episode)
