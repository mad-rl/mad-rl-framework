Gym Atari Breakout Actor-Critic Agent with Policy Gradient
===

## Install dependencies

There is a requirements.txt file with the dependencies in the enviroenment gym_atari, we recommend to use virtualenv in order to isolate these dependencies from any other you already have in your system.

```
pip install -f ./src/environments/gym_atari/requirements.txt
```

### Agents

#### Breakout Actor-Critic Policy Gradient

```
PYTHONPATH=./src/ ENGINE_MODULE=environments.gym_atari.engine AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent GAME=BreakoutDeterministic-v4 python3.6 ./src/environments/main.py
```

#### Breakout Actor-Critic DQN

```
PYTHONPATH=./src/ ENGINE_MODULE=environments.gym_atari.engine AGENT_MODULE=environments.gym_atari.breakout_actor_critic_dqn.agent GAME=BreakoutDeterministic-v4 python3.6 ./src/environments/main.py
```
