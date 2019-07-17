import os


CONFIG = {
    "train": bool(os.getenv('TRAIN', True)),
    "test": bool(os.getenv('TEST', False)),
    "episodes": int(os.getenv('EPISODES', 10)),
    "steps_per_episode": int(os.getenv('STEPS_PER_EPISODE', 100)),
    "engine": {
        "module": os.getenv('ENGINE_MODULE',
                            'environments._test_env.test_engine'),
        "class": os.getenv('ENGINE_CLASS', 'Engine')
    },
    "agent": {
        "module": os.getenv('AGENT_MODULE',
                            'environments._test_env._test_agent.agent'),
        "class_name": os.getenv('AGENT_CLASS', 'Agent')
    }
}

print("config: ", CONFIG)


class MAD_RL:

    @staticmethod
    def config():
        return CONFIG.copy()

    @staticmethod
    def engine(module=None, class_name=None):
        config = MAD_RL.config()
        if module is None:
            module = config["engine"]["module"]
        if class_name is None:
            class_name = config["engine"]["class"]
        environment_module = __import__(module, fromlist=["*"])
        environment_class = getattr(environment_module, class_name)
        return environment_class()

    @staticmethod
    def agent(module=None, class_name=None, action_space=None):
        config = MAD_RL.config()
        if module is None:
            module = config["agent"]["module"]
        if class_name is None:
            class_name = config["agent"]["class_name"]
        agent_mod = __import__(module, fromlist=["*"])
        agent_class = getattr(agent_mod, class_name)
        return agent_class(action_space)
