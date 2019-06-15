Gym Atari Breakout Actor-Critic Agent with Policy Grading
===

## Install dependencies

There is an conda env file with the dependencies for run this agent

```
conda env update -f ./breakout_actor_critic_policy_env.yml
```

## Run this agent

```
PYTHONPATH=./src/ GAME=BreakoutDeterministic-v4 AGENT_MODULE=environments.gym.breakout_actor_critic_policy.agent python ./src/environments/gym/train_agent.py
```

