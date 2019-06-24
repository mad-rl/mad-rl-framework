Gym Retro
===

## Install dependencies

There is a requirements.txt file with the dependencies in the enviroenment gym_retro, we recommend to use virtual environment such as pipenv, virtualenv or conda in order to isolate these dependencies from any other you already have in your system or other engines.

```
pip install -f ./src/environments/gym_retro/requirements.txt
```

### Agents

#### SFII Actor-Critic

```
PYTHONPATH=./src/ ENGINE_MODULE=environments.gym_retro.engine AGENT_MODULE=environments.gym_retro.sf2_actor_critic_policy.agent GAME=StreetFighterIISpecialChampionEdition-Genesis python ./src/environments/main.py
```
