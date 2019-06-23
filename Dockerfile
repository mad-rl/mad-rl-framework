FROM ubuntu:18.04

COPY . ./mad_rl

RUN apt update && apt -y install python3.6 python3-pip xvfb python-opengl

RUN pip3 install gym

RUN pip3 install gym[atari]

RUN pip3 install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp36-cp36m-linux_x86_64.whl

RUN pip3 install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

ENV PYTHONPATH /mad_rl/src/

CMD [ "python3.6", "/mad_rl/src/environments/main.py" ]

# docker run -e ENV_RENDER=False -e ENV_MODULE=environments.gym_atari.train_agent e- AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent e- GAME=BreakoutDeterministic-v4 mad_rl:0.1.4
# docker run -e GAME=BreakoutDeterministic-v4 -e ENV_RENDER=False mad_rl:0.1.3
# docker run -e ENV_RENDER=False -e ENV_MODULE=environments.gym_atari.train_agent AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent -e GAME=BreakoutDeterministic-v4 mad_rl:0.1.5
# PYTHONPATH=./src/ ENV_MODULE=environments.gym_atari.train_agent AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent GAME=BreakoutDeterministic-v4 python3.6 ./src/environments/main.py
# ENGINE_MODULE=environments.gym_atari.engine AGENT_MODULE=environments.gym_atari.breakout_actor_critic_policy.agent GAME=BreakoutDeterministic-v4 /usr/bin/xvfb-run -s '-screen 0 1024x768x16' python3.6 /mad_rl/src/environments/main.py
