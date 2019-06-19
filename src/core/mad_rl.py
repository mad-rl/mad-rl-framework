import os


CONFIG = {
            "episodes": int(os.getenv('EPISODES', 10)),
            "steps_per_episode": int(os.getenv('STEPS_PER_EPISODE', 100)),
            "environment": {
                "training_module": os.getenv('TRAINING_MODULE', 'environments._test_env.train_agent'),
                "training_class": os.getenv('TRAINING_CLASS', 'Environment')
            },
            "agent": {
                "module": os.getenv('AGENT_MODULE', 'environments._test_env._test_agent.agent'),
                "class_name": os.getenv('AGENT_CLASS', 'Agent')
            }
        }

print("config: ",CONFIG)

class MAD_RL:

    @staticmethod
    def config():
        return CONFIG.copy()

    @staticmethod
    def env(module=None, class_name=None):
        if module == None:
            module = MAD_RL.config()["environment"]["training_module"]
        if class_name == None:
            class_name = MAD_RL.config()["environment"]["training_class"]
        environment_module = __import__(module, fromlist=["*"])
        environment_class = getattr(environment_module, class_name)
        return environment_class()

    @staticmethod
    def agent(module=None, class_name=None, action_space=[]):
        if module == None:
            module = MAD_RL.config()["agent"]["module"]
        if class_name == None:
            class_name = MAD_RL.config()["agent"]["class_name"]
        agent_mod = __import__(module, fromlist=["*"])
        agent_class = getattr(agent_mod, class_name)
        return agent_class(action_space)
