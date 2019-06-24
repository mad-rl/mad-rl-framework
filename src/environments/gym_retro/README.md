Gym Atari Breakout Actor-Critic Agent with Policy Grading
===

## Install dependencies

There is a requirements.txt file with the dependencies in the enviroenment gym_retro, we recommend to use virtual environment such as pipenv, virtualenv or conda in order to isolate these dependencies from any other you already have in your system or other engines.

```
pip install -f ./src/environments/gym_retro/requirements.txt
```

### Agents

#### SFII Asynchronous Actor-Critic

```
PYTHONPATH=./src/ ENGINE_MODULE=environments.gym_retro.engine AGENT_MODULE=environments.gym_retro.sfii_a3c.agent GAME=StreetFighterIISpecialChampionEdition-Genesis python3.6 ./src/environments/main.py
```
