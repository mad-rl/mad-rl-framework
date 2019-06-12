Street Fighter 2 Gym Retro Environment
===

This environment uses OpenAI Gym Retro to allow implement RL algorithms easily for the Genesis version of Street Fighter 2.

## Architecture

We have split the environment in different components trying to simplify the implementation of new algorithms. These components are very common in most of the RL approaches.

The main idea of this approach is to ensure that the agent will be trained in a way that will work in an inference environment. This is very important because depending on the context the agent won't access to the same information during the training than in the runtime.

![RL Agent Environment Training Loop](./images/mad_rl_scheme_training.png)


![RL Agent Environment Runtime](./images/mad_rl_scheme_runtime.png)


### Components Summary

The components we have split the framework are:

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

## Run

```
PYTHONPATH=./src/ python ./src/algorithms/_new_template/train_agent.py
```


