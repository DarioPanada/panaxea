from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper

"""
A very simple model which illustrates the basis of creating a model.

An instance of the model is created specifying it will run for 10 epochs.

A class is defined for a SimpleAgent which, in the prologue, outputs its
name. In the epilogue, it outputs the model property counter.

A helper is created which once at the end of each epoch increases the counter
by 1.

Finally, two SimpleAgents and an instance of the helper are added to the
schedule and the model is run.
"""


class SimpleAgent(Agent):
    """
    SimpleAgent class, a trivial agent that has a name and reads model
    properties.

    Attributes
    ----------
    name : string
        The agent's name
    """

    def __init__(self, name):
        super(SimpleAgent, self).__init__()
        self.name = name

    def step_prologue(self, model):
        print("This is the prologue, so I will say my name: {0}".format(
            self.name))

    def step_epilogue(self, model):
        print("This is the epilogue, and {0} says the counter is set to"
              " {1}".format(self.name, model.properties["counter"]))


class SimpleHelper(Helper):

    def step_prologue(self, model):
        model.properties["counter"] += 1


model = Model(10)
model.properties["counter"] = 0

model.schedule.agents_to_schedule.add(SimpleAgent("Adam"))
model.schedule.agents_to_schedule.add(SimpleAgent("Beth"))
model.schedule.helpers.append(SimpleHelper())

model.run()
