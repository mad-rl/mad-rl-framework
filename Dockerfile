FROM ubuntu:18.04

RUN apt update && apt -y install python3.7 python3-pip git python-opengl xvfb

RUN python3.7 -m pip install gym[atari]
RUN python3.7 -m pip install gym-retro
RUN python3.7 -m pip install s2clientprotocol

WORKDIR /mad-rl-framework/
COPY . .

ENV PYTHONPATH  ./src/

CMD [ "python3.7", "./src/environments/main.py" ]


# docker run -e ENV_MODULE=environments.gym_atari.train_agent -e AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent e- GAME=BreakoutDeterministic-v4 madrl-cpu:local