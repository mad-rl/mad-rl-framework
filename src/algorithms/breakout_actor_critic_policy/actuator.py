from agent_base.actuator_base import ActuatorBase

class Actuator(ActuatorBase):
    
    def __init__(self):
        ActuatorBase.__init__(self)

    def model_to_env(self, model_action):
        return model_action.item() + 1

    def env_to_model(self, env_action):
        return env_action - 1

