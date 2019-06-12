from agent_base.knowledge_base import KnowledgeBase

class Knowledge(KnowledgeBase):
    
    def __init__(self, action_space=None):
        KnowledgeBase.__init__(self, action_space)

    def get_action(self):
        pass