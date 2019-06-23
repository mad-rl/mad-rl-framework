MAD_RL_ Framework (Work in Progress)
===

This framework borned in paralel to the starting of the [MAD_RL_](https://www.meetup.com/MAD_RL/) collective. A group of people interested on Reinforcement Learning area within Artificial Intelligence. MAD_RL_ shares the idea that RL and other semi-supervised learning techniques will require experience from many different fields to evolve. Some obvious such as Mathematics or Software Engineering, but also others less obvious such as Psychology, Neuroscience and others even more distant as Philosophy or Sociology, just to name a few.

The goal of this framework is to allow researchers and practiotioners to have a pretty clear architecture from the point of view of the RL concepts, and also being totally agnostic from libraries and environments.

## Architecture

We have split the environment in different components trying to simplify the implementation of new algorithms. These components are very common in most of the RL approaches.

The main idea of this approach is to isolate the different components to let the coder focus on one component at a time. Also this approach ensures that the agent will be trained in a way that will work in an inference environment. This is very important because depending on the context the agent won't access to the same information during the training than in the runtime.

### Training Loop
![RL Agent Environment Training Loop](./images/mad_rl_scheme_training.png)

### Runtime
![RL Agent Environment Runtime](./images/mad_rl_scheme_runtime.png)


### Components Summary

The components within the framework are:

#### The Environment Engine
 * **Engine:** An engine define how the agents will interact with the environment. We currently have Gym[Atari] and Retro already implemented with several agents and algorithms working.

#### The Agent

 * **Agent:** The base define an interface that should be able to integrate in any RL environment.
 * **Sensors:** The sensors are the different ways to get information from the environment in a runtime context.
 * **Interpreters:** The interpreters are a bridge between Sensors and other parts of the agent. They transform the information taken by the Sensors and apply any transformation or process to provide the information ready to use.
 * **Actuators:** The actuators translate the agent decisions into something comprehensible by the environment.
 * **Experiences:** The experiences are very related with the RL approach / algorithm used. Although the concept is almost always the same, this component allows to isolate the experience approach.
 * **Knowledge:** The knowledge is where the algorithm must be implemented, here the learning must be saved and accessed in order to take decisions.

## Installation

### Engine requirements

Each engine has its own requirements. We recommend to use a virtual environment such a pipenv, virtualenv or conda in order to isolate the specific requirements of each engine from your current libraries or other engines.

```
pip install -f ./src/environments/{environment_name}/requirements.txt
```

### Test the environment

```
PYTHONPATH=./src/ ENGINE_MODULE=environments._test_env.test_engine AGENT_MODULE=environments._test_env._test_agent.agent python ./src/environments/main.py
```

## Environments

### Gym[Atari]

The OpenAI Gym is one of the standars to apply RL algorithms in videogames. This enviroment is focused on Atari games.

[Gym Atari](./src/environments/gym_atari/README.md)

### (Work in Progress) Gym[Retro]

The OpenAI Gym Retro is the same than Gym Atari but using 8bit/16bit consoles emulators to apply RL algorithms in that videogames.

[Gym Retro](./src/environments/gym_retro/README.md)
