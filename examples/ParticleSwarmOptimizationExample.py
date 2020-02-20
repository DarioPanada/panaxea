"""
A simple two-dimensional particle swarm optimization. A target position is
specified together with a number of particles/agents and a number of
iterations. Eventually, the particles identify the target position.
"""

import math
from random import random

import matplotlib.pyplot as plt
from numpy.random import randint

from panaxea.core.Environment import ObjectGrid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper


class PSOAgent(Agent):
    """
    Simple particle swarm optimization agent implementation.

    Attributes
    ----------
    position : tuple
        A tuple specifying an x and y coordinate.
    """

    def __init__(self, position):
        super(PSOAgent, self).__init__()
        self.position = position
        self.bestFit = 0

    def step_prologue(self, model):
        # We get the fitness as proportional to the euclidean distance between
        # the target and current position.

        # If the exit flag is true then it means another agent found the
        # target position, no need to do anything.
        if model.exit:
            return

        # If we found the target position no ned to do anything else.
        if self.position == model.properties["target_position"]:
            model.properties["best_position"] = self.position
            model.exit = True
            return

        fitness = 1. / math.sqrt(
            (model.properties["target_position"][0] - self.position[0]) ** 2 +
            (model.properties["target_position"][1] - self.position[1]) ** 2)

        # Have we found a better position? If so, we keep track of it.
        if fitness > self.bestFit:
            self.bestFit = fitness

        # Have we found a better position than anybody else? If so, we store
        # it in the model.
        if fitness > model.properties["best_fitness"]:
            model.properties["best_fitness"] = fitness
            model.properties["best_position"] = self.position

    def step_main(self, model):

        if model.exit:
            return

        agent_env = model.environments["agent_env"]

        # We add some noise to prevent all agents from just flocking to the
        # one that, by chance, initially was closest to the target
        noise = 5

        targetx = model.properties["best_position"][0] + randint(-1 * noise,
                                                                 noise + 1)
        targety = model.properties["best_position"][1] + randint(-1 * noise,
                                                                 noise + 1)

        maxx = agent_env.xsize - 1
        maxy = agent_env.ysize - 1

        selfx = self.position[0]
        selfy = self.position[1]

        xdistance = abs(selfx - targetx)
        ydistance = abs(selfy - targety)

        # We move closer to the best found position by a fraction of the
        # distance
        xdisplacement = random() * xdistance
        ydisplacement = random() * ydistance

        # Preventing off-grid destination positions
        if selfx > targetx:
            selfx -= xdisplacement
        else:
            selfx += xdisplacement

        if selfy > targety:
            selfy -= ydisplacement
        else:
            selfy += ydisplacement

        if selfx < 0:
            selfx = 0

        if selfx > maxx:
            selfx = maxx

        if selfy < 0:
            selfy = 0

        if selfy > maxy:
            selfy = maxy

        # Positions must be whole numbers, so we round
        self.position = (round(selfx), round(selfy))
        self.move_agent("agent_env", self.position, model)


class FitnessTrackerHelper(Helper):

    def __init__(self):
        super(FitnessTrackerHelper, self).__init__()

    def step_epilogue(self, model):
        model.output["best_fitness_in_epochs"] \
            .append(model.properties["best_fitness"])


epochs = 50

model = Model(epochs)

xsize = ysize = 500
ObjectGrid2D("agent_env", xsize, ysize, model)
target_position = (12, 12)

model.properties = {
    "best_fitness": 0,  # setting global best to 0
    "best_position": (0, 0),
    "target_position": target_position
}

model.output = {
    "best_fitness_in_epochs": []
}

num_agents = 20

for _ in range(num_agents):
    agent_position = (randint(0, xsize), randint(0, ysize))
    agent = PSOAgent(agent_position)

    model.schedule.agents.add(agent)
    agent.add_agent_to_grid("agent_env", agent_position, model)

model.schedule.helpers.append(FitnessTrackerHelper())

model.run()
plt.figure()
plt.scatter(range(model.current_epoch + 1), model.output[
    "best_fitness_in_epochs"])
plt.xlabel("Epoch")
plt.ylabel("Best Fitness")
plt.title("Best Fitness across Epochs")
plt.show()

print("Best fitness obtained: {0}".format(
    model.output["best_fitness_in_epochs"][-1]))
print("Best position found: {0}".format(model.properties["best_position"]))
