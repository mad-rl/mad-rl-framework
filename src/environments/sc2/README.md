SC2
===

## Install dependencies

There is a requirements.txt file with the dependencies in the enviroenment gym_retro, we recommend to use virtual environment such as pipenv, virtualenv or conda in order to isolate these dependencies from any other you already have in your system or other engines.

```
pip install -r ./src/environments/gym_retro/requirements.txt
```

### Agents

#### SC2 Base Agent

```
PYTHONPATH=./src/ ENGINE_MODULE=environments.sc2.engine AGENT_MODULE=environments.sc2.base_agent.agent python ./src/environments/main.py
```
