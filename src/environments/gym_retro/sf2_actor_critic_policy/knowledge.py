import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class ActorCritic(torch.nn.Module):
    def __init__(self, num_inputs=4, num_outputs=4):
        super(ActorCritic, self).__init__()

        self.model_structure(num_inputs, num_outputs)
        self.train()

    def model_structure(self, num_inputs, num_outputs):
        self.conv1 = nn.Conv2d(num_inputs, 32,
                               kernel_size=2, stride=2, padding=1)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=2, stride=2, padding=1)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=2, stride=2, padding=1)
        self.conv4 = nn.Conv2d(32, 32, kernel_size=2, stride=2, padding=1)
        self.conv5 = nn.Conv2d(32, 32, kernel_size=2, stride=2, padding=1)

        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(512, 120)

        self.value = nn.Linear(120, 1)
        self.policy = nn.Linear(120, num_outputs)

    def forward(self, inputs):
        x = self.relu(self.conv1(inputs))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = self.relu(self.conv5(x))

        x = x.view(-1, 512)

        x = self.relu(self.fc1(x))

        return self.policy(x), self.value(x)


class Knowledge():
    def __init__(self, input_frames, action_space):
        self.input_frames = input_frames
        self.action_space = action_space
        self.model = ActorCritic(self.input_frames, self.action_space)
        self.model.double()
        self.model.train()

        self.gamma = 0.9
        self.tau = 1.0
        self.entropy_coef = 0.01
        self.value_loss_coef = 0.5
        self.learning_rate = 0.00001

        self.optimizer = optim.Adam(
            self.model.parameters(), lr=self.learning_rate
        )
        self.model = self.model.to('cpu')

    def load_shared_model(self, shared_model):
        self.shared_model = shared_model
        self.model.load_state_dict(self.shared_model.state_dict())

    def reload_model(self):
        self.model.load_state_dict(self.shared_model.state_dict())

    def ensure_shared_grads(self):
        for param, shared_param in zip(self.model.parameters(),
                                       self.shared_model.parameters()):
            if shared_param.grad is not None:
                return
            shared_param._grad = param.grad

    def get_action(self, state):
        policy, _ = self.model(torch.tensor(state).unsqueeze(0))
        action = F.softmax(policy, -1).multinomial(num_samples=1)
        return action

    def train(self, experiences):
        states = torch.tensor(experiences[:, 0].tolist()).double()
        rewards = torch.tensor(experiences[:, 1].tolist()).double()
        actions = torch.tensor(experiences[:, 2].tolist()).long()
        next_states = torch.tensor(experiences[:, 3].tolist()).double()

        logits, values = self.model(states)
        probs = F.softmax(logits, -1)
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
            delta_t = (
                rewards[i] +
                self.gamma * values[i + 1].data -
                values[i].data)
            gae = gae.double() * self.gamma * self.tau + delta_t
            policy_loss = (
                policy_loss -
                (log_probs[i] * gae) -
                (self.entropy_coef * entropies[i]))

        self.optimizer.zero_grad()
        loss_fn = (policy_loss + self.value_loss_coef * value_loss)
        loss_fn.backward()
        self.ensure_shared_grads()
        self.optimizer.step()

        torch.save(self.shared_model.state_dict(), 'sf2_a3c.pth')
