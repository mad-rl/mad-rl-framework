MAD_RL_ Framework
===

This framework borned in paralel to the starting of the [MAD_RL_](https://www.meetup.com/MAD_RL/) collective. A group of people interested on Reinforcement Learning area within Artificial Intelligence. MAD_RL_ shares the idea that RL and other semi-supervised learning techniques will require experience from many different fields to evolve. Some obvious such as Mathematics or Software Engineering, but also others less obvious such as Psychology, Neuroscience and others even more distant as Philosophy or Sociology, just to name a few.

The goal of this framework is to allow researchers and practiotioners to have a pretty clear architecture from the point of view of the RL concepts, and also beaing totally agnostic from libraries and environments.

## Architecture

We have split the environment in different components trying to simplify the implementation of new algorithms. These components are very common in most of the RL approaches.

The main idea of this approach is to ensure that the agent will be trained in a way that will work in an inference environment. This is very important because depending on the context the agent won't access to the same information during the training than in the runtime.

### Training Loop
![RL Agent Environment Training Loop](./images/mad_rl_scheme_training.png)

### Runtime
![RL Agent Environment Runtime](./images/mad_rl_scheme_runtime.png)


### Components Summary

The components we have split the framework are:

#### The Environment
 * **Environment:** An environment define the rules where the agents will interact.
 

#### The Agent

 * **AgentBase:** The base define an interface that should be able to integrate in any RL environment.
 * **Sensors:** The sensors are the different way to get information from the environment in a runtime context.
 * **Interpreters:** The interpreters are a bridge between Sensors and other parts of the agent, they transforms the information taken by the sensors and apply any transformation or process to provide other parts in the agent the information ready to use.
 * **Actuators:** The actuators translate the agent decisions into something comprehensible by the environment.
 * **Experiences:** The experiences are very related with the RL approach / algorithm used. However the concept is almost alway the same, this component allows to isolate the experience approach.
 * **Knowledge:** The knowledge is where the algorithm must be implemented, here the learning must be saved and accessed in order to take decisions.

#### The Environment

In this case we have implemented the framwork using OpenAI Gym creating a train loop script and a testing script.

## Installation

```
conda env create -f madrl_retro_gym_conda_env.yml
```

### Test installation

Firs of all, ensure you have the right conda environment active:

```
conda activate mad_rl_framework
```

A default AGENT and ENVIRONMENT are inside **environments/_new_env_template**, you can test it with the following command:

```
PYTHONPATH=./src/ AGENT_MODULE=environments._new_env_template._new_agent.agent python ./src/environments/_new_env_template/train_agent.py
```

## Create your own Agent for an existing Environment

In order to create a new agent, copy the entire folder **./src/environments/_new_template/** and rename it with yours, implement your algorithm and run it using the same command but changing the module and path for yours, eg:

```
cp ./src/agents/_new_template/ ./src/agents/my_environment/my_agent/
PYTHONPATH=./src/ AGENT_MODULE=agents.my_environment.my_agent.agent python ./src/agent/my_environment/train_agent.py
```

You can also find agents already implemented for Gym such as Breakout Actor-Critic Policy Agent, the command to run it is:

```
PYTHONPATH=./src/ GAME=Break AGENT_MODULE=agents.gym.breakout_actor_critic_policy.agent python ./src/agents/gym/train_agent.py
```

## Create your own Environment


