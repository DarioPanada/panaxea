from panaxea.core.Steppables import Agent, Helper


class SimpleAgent(Agent, object):

    def __init__(self):
        super(SimpleAgent, self).__init__()
        self.a = 0

    def step_prologue(self, model):
        pass

    def step_main(self, model):
        self.a += 1

    def step_epilogue(self, model):
        pass


class SimpleHelper(Helper, object):

    def __init__(self):
        super(SimpleHelper, self).__init__()

    def step_prologue(self, model):
        pass

    def step_main(self, model):
        pass

    def step_epilogue(self, model):
        for agent in model.schedule.agents:
            agent.a *= 2


class SampleAgent(Agent, object):

    def __init__(self):
        super(SampleAgent, self).__init__()
        self.a = 0
        self.b = 1
        self.c = 2

    def step_prologue(self, model):
        self.a += 1

    def step_main(self, model):
        self.b += 2

    def step_epilogue(self, model):
        self.c += 3


class SampleHelper(Helper, object):
    def __init__(self):
        super(SampleHelper, self).__init__()

    def step_prologue(self, model):
        self.x = 10

    def step_main(self, model):
        self.y = 11

    def step_epilogue(self, model):
        self.z = 12


class AgentX(Agent, object):
    def __init__(self):
        super(AgentX, self).__init__()
        self.flag = None


class AgentY(Agent):
    pass


class AgentZ(Agent):
    pass
