import gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.distributions.categorical import Categorical
from agent_base.knowledge_base import KnowledgeBase


class CnnNetwork(nn.Module):
    def __init__(self):
        super(CnnNetwork, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, 8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, 3, stride=1)

        self.fc1 = nn.Linear(7 * 7 * 64, 512)
        self.fc2 = nn.Linear(512, 512)

        self.actor  = nn.Linear(512, 3)
        self.critic = nn.Linear(512, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        x = x.view(-1, 7 * 7 * 64)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        policy = self.actor(x)
        value  = self.critic(x)

        return policy, value


class Knowledge(KnowledgeBase):
    def __init__(self, action_space):
        KnowledgeBase.__init__(self, action_space)

        self.model = CnnNetwork()
        self.model.double()

        self.gamma = 0.9
        self.tau = 1.0
        self.entropy_coef = 0.01
        self.value_loss_coef = 0.5
        self.learning_rate = 0.00001

        self.optimizer = optim.Adam(
            self.model.parameters(), lr=self.learning_rate)
        self.model = self.model.to('cpu')

    def get_action(self, state):
        policy, _ = self.model(torch.tensor(state).unsqueeze(0))
        action = F.softmax(policy, -1).multinomial(num_samples=1)

        return action

    def train(self, experiences):
        states  = torch.tensor(experiences[:, 0].tolist()).double()
        rewards = torch.tensor(experiences[:, 1].tolist()).double()
        actions = torch.tensor(experiences[:, 2].tolist()).long()
        next_states = torch.tensor(experiences[:, 3].tolist()).double()

        logits, values = self.model(states)
        probs     = F.softmax(logits, -1)
        log_probs = F.log_softmax(logits, -1)
        entropies = -(log_probs * probs).sum(1, keepdim=True)
        log_probs = log_probs.gather(1, actions.unsqueeze(1))

        _, value = self.model(next_states[-1].unsqueeze(0))
        values = torch.cat((values, value.data))

        policy_loss = 0
        value_loss = 0
        R = values[-1]
        gae = torch.zeros(1, 1)
        for i in reversed(range(len(rewards))):
            R = self.gamma * R + rewards[i]
            advantage = R - values[i]
            value_loss = value_loss + 0.5 * advantage.pow(2)

            # Generalized Advantage Estimation
            delta_t = rewards[i] + self.gamma * values[i + 1].data - values[i].data
            gae = gae.double() * self.gamma * self.tau + delta_t
            policy_loss = policy_loss - (log_probs[i] * gae) - (self.entropy_coef * entropies[i])

        self.optimizer.zero_grad()
        loss_fn = (policy_loss + self.value_loss_coef * value_loss)
        loss_fn.backward()
        self.optimizer.step()