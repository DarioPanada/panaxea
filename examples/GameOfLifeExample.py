"""
A simple implementation of Conway's Game of Life. The grid is randomly
initialized at each epoch with agents having an equal probability of being
on or off.

Requires Matplotlib and Numpy to be installed.
"""
import time
from random import random

import matplotlib.pyplot as plt
import numpy as np

from panaxea.core.Environment import ObjectGrid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent, Helper


class GOLAgent(Agent):
    """
    Simple Game of Life Agent that checks its neighbourhood and decides if
    it should be alive or dead accordingly.

    Attributes
    ----------
    alive : bool
        The initial state of the agent.
    """

    def __init__(self, alive):
        super(GOLAgent, self).__init__()
        self.alive = alive

    def step_main(self, model):
        current_position = self.environment_positions["agent_env"]
        neighbourhood = model.environments[
            "agent_env"].get_moore_neighbourhood(current_position)

        alive_neighbours = 0

        for neighbour in neighbourhood:
            # A bit of python magic to get the agent at each position
            neighbour_state = next(iter(model.environments["agent_env"].grid[
                                            neighbour])).alive
            if neighbour_state:
                alive_neighbours += 1

        # Any live cell with fewer than two live neighbours dies, as if by
        # underpopulation.
        if self.alive and alive_neighbours < 2:
            self.alive = False
        # Any live cell with two or three live neighbours lives on to the
        # next generation.
        elif self.alive and alive_neighbours in [2, 3]:
            pass
        # Any live cell with more than three live neighbours dies, as if by
        # overpopulation.
        elif self.alive and alive_neighbours > 3:
            self.alive = False
        # Any dead cell with exactly three live neighbours becomes a live cell,
        # as if by reproduction.
        elif not self.alive and alive_neighbours == 3:
            self.alive = True


class RenderHelper(Helper):
    """
    A simple renderer that, at each epoch, displays a heatmap of agents
    which are on/off.
    """

    def __init__(self):
        super(Helper, self).__init__()

    def step_epilogue(self, model):

        agent_env = model.environments["agent_env"]

        grid = np.zeros((agent_env.xsize, agent_env.ysize))

        positions = agent_env.grid.keys()

        for position in positions:
            if next(iter(agent_env.grid[(position[0], position[1])])).alive:
                grid[position[0]][position[1]] = 1
            else:
                grid[position[0]][position[1]] = 0

        plt.figure()
        plt.imshow(grid)
        plt.show()
        time.sleep(0.1)


model = Model(100)

# Change these to change the size of the environment.
xsize = ysize = 10

ObjectGrid2D("agent_env", xsize, ysize, model)

for x in range(xsize):
    for y in range(ysize):
        agent = GOLAgent(random() <= 0.5)
        agent.add_agent_to_grid("agent_env", (x, y), model)
        model.schedule.agents.add(agent)

model.schedule.helpers.append(RenderHelper())

model.run()
