"""
A simple model which introduces the use of an ObjectGrid Environment to hold
an agent and a numerical environment to hold values. The agent moves through
the environment and reads off values.
"""
from panaxea.core.Environment import ObjectGrid2D, NumericalGrid2D
from panaxea.core.Model import Model
from panaxea.core.Steppables import Agent


class SimpleAgent(Agent):

    def __init__(self):
        super(SimpleAgent, self).__init__()
        self.add_agent_to_grid("agent_env", (0, 0), model)
        self.end_of_grid = False

    def step_main(self, model):
        current_position = self.environment_positions["agent_env"]
        grid_value = model.environments["value_env"].grid[current_position]

        print("Value at position ({0}, {1}) is {2}".format(
            current_position[0], current_position[1], grid_value))

        self.__move_to_next_position(model)

    def __move_to_next_position(self, model):
        """
        Moves the agent to the next position in the grid. Movement occurs
        along the x-axis, once the end of the x-axis is reached it proceeds
        to th next y-axis position until the end of the grid is reached.
        Then the agent stops.
        Parameters
        ----------
        model : Model
            The current model instance
        """

        if self.end_of_grid:
            return

        current_position = self.environment_positions["agent_env"]

        xlimit = model.environments["agent_env"].xsize - 1
        ylimit = model.environments["agent_env"].ysize - 1

        if current_position == (xlimit, ylimit):
            self.end_of_grid = True
            return

        if current_position[0] == xlimit:
            new_position = (0, current_position[1] + 1)
        else:
            new_position = (current_position[0] + 1, current_position[1])

        self.move_agent("agent_env", new_position, model)


xsize = ysize = 20

model = Model(xsize * ysize + 5)

# Creating the grid automatically binds it to the model
ObjectGrid2D("agent_env", xsize, ysize, model)
numerical_env = NumericalGrid2D("value_env", xsize, ysize, model)

# Adding the agent to the schedule and to the environment
agent = SimpleAgent()
model.schedule.agents.add(agent)
agent.add_agent_to_grid("agent_env", (0, 0), model)
val = 0

for y in range(ysize):
    for x in range(xsize):
        numerical_env.grid[(x, y)] = val
        val += 1

model.run()
