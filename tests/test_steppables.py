import unittest

from panaxea.core.Environment import ObjectGrid2D, ObjectGrid3D
from panaxea.core.Model import Model
from tests.resources.SampleSteppables import AgentX, SimpleAgent


class TestSteppables(unittest.TestCase):

    def test_remove_agent(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        grid_name = "sampleGridA"
        grid_name_b = "sampleGridB"

        env = ObjectGrid2D(grid_name, xsize, ysize, model)
        env_b = ObjectGrid2D(grid_name_b, xsize, ysize, model)
        pos = (5, 5)
        pos_b = (5, 6, 7)
        a = AgentX()

        a.add_agent_to_grid(grid_name, pos, model)
        a.add_agent_to_grid(grid_name_b, pos_b, model)

        model.schedule.agents.add(a)

        self.assertEqual(1, env.grid[pos].__len__())
        self.assertEqual(1, env_b.grid[pos_b].__len__())

        self.assertEqual(pos, a.environment_positions[grid_name])
        self.assertEqual(pos_b, a.environment_positions[grid_name_b])

        a.remove_agent(model)

        self.assertIsNone(a.environment_positions[grid_name])
        self.assertIsNone(a.environment_positions[grid_name_b])

        self.assertEqual(0, env.grid[pos].__len__())
        self.assertEqual(0, env_b.grid[pos_b].__len__())
        self.assertEqual(a, model.schedule.agents_to_remove.pop())

    def test_remove_agent_from_grid(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        grid_name = "sampleGridA"

        env = ObjectGrid2D(grid_name, xsize, ysize, model)

        pos = (5, 5)

        a = AgentX()
        a.add_agent_to_grid(grid_name, pos, model)
        self.assertEqual(1, env.grid[pos].__len__())
        self.assertEqual(pos, a.environment_positions[grid_name])
        a.remove_agent_from_grid(grid_name, model)
        self.assertEqual(0, env.grid[pos].__len__())
        self.assertIsNone(a.environment_positions[grid_name])

    def test_remove_agent_grid_2d(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        grid_name = "sampleGridA"

        env = ObjectGrid2D(grid_name, xsize, ysize, model)

        pos = (5, 5)

        a = AgentX()
        a.add_agent_to_grid(grid_name, pos, model)
        self.assertEqual(1, env.grid[pos].__len__())
        env.remove_agent(a, pos)
        self.assertEqual(0, env.grid[pos].__len__())

    def test_add_agent_to_grid(self):
        model = Model(5)
        grid_name = "sampleGridB"
        ObjectGrid2D(grid_name, 10, 10, model)

        agent = SimpleAgent()

        position = (5, 6)

        agent.add_agent_to_grid(grid_name, position, model)

        self.assertEqual(agent.environment_positions[grid_name], position)
        self.assertEqual(model.environments[grid_name].grid[position].pop(),
                         agent)

    def test_move_agent_valid(self):
        model = Model(5)
        grid_name = "sampleGridB"

        ObjectGrid2D(grid_name, 20, 20, model)

        agent = SimpleAgent()

        position = (5, 6)

        agent.add_agent_to_grid(grid_name, position, model)

        position_b = (6, 7)

        agent.move_agent(grid_name, position_b, model)

        self.assertEqual(agent.environment_positions[grid_name], position_b)
        self.assertEqual(len(model.environments[grid_name].grid[position]), 0)
        self.assertEqual(len(model.environments[grid_name].grid[position_b]),
                         1)

        position_c = (9, 9)

        agent.move_agent(grid_name, position_c, model)

        self.assertEqual(agent.environment_positions[grid_name], position_c)
        self.assertEqual(len(model.environments[grid_name].grid[position_b]),
                         0)
        self.assertEqual(model.environments[grid_name].grid[position_c].pop(),
                         agent)

    def test_add_agent_invalid(self):
        model = Model(5)
        grid_name = "sampleGridB"

        ObjectGrid2D(grid_name, 20, 20, model)

        agent = SimpleAgent()

        position = (50, 50)

        agent.add_agent_to_grid(grid_name, position, model)

        self.assertEqual(len(agent.environment_positions), 0)

    def test_move_agent_invalid(self):
        model = Model(5)
        grid_name = "sampleGridB"

        ObjectGrid2D(grid_name, 20, 20, model)

        agent = SimpleAgent()

        position = (5, 6)

        agent.add_agent_to_grid(grid_name, position, model)

        position_b = (50, 55)

        agent.move_agent(grid_name, position_b, model)

        self.assertEqual(agent.environment_positions[grid_name], position)
        self.assertEqual(model.environments[grid_name].grid[position].pop(),
                         agent)

    # Tests for ObjectGrid3D

    def test_remove_agent_grid_ed(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        zsize = 25
        grid_name = "sampleGridA"

        env = ObjectGrid3D(grid_name, xsize, ysize, zsize, model)

        pos = (5, 5, 5)

        a = AgentX()
        a.add_agent_to_grid(grid_name, pos, model)
        self.assertEqual(1, env.grid[pos].__len__())
        env.remove_agent(a, pos)
        self.assertEqual(0, env.grid[pos].__len__())

    def test_add_agent_to_grid_3d(self):
        model = Model(5)
        grid_name = "sampleGrid3DB"

        ObjectGrid3D(grid_name, 20, 20, 20, model)

        agent = SimpleAgent()

        position = (5, 6, 7)

        agent.add_agent_to_grid(grid_name, position, model)

        self.assertEqual(agent.environment_positions[grid_name], position)
        self.assertEqual(model.environments[grid_name].grid[position].pop(),
                         agent)

    def test_move_agent_valid_3d(self):
        model = Model(5)
        grid_name = "sampleGrid3DC"

        ObjectGrid3D(grid_name, 20, 20, 20, model)

        agent = SimpleAgent()

        position = (5, 6, 7)

        agent.add_agent_to_grid(grid_name, position, model)

        position_b = (6, 7, 8)

        agent.move_agent(grid_name, position_b, model)

        self.assertEqual(agent.environment_positions[grid_name], position_b)
        self.assertEqual(len(model.environments[grid_name].grid[position]), 0)
        self.assertEqual(len(model.environments[grid_name].grid[position_b]),
                         1)

        positionC = (9, 9, 9)

        agent.move_agent(grid_name, positionC, model)

        self.assertEqual(agent.environment_positions[grid_name], positionC)
        self.assertEqual(len(model.environments[grid_name].grid[position_b]),
                         0)
        self.assertEqual(model.environments[grid_name].grid[positionC].pop(),
                         agent)

    def test_add_agent_invalid_3d(self):
        model = Model(5)
        grid_name = "sampleGridC3D"

        ObjectGrid3D(grid_name, 20, 20, 20, model)

        agent = SimpleAgent()

        position = (50, 50, 50)

        agent.add_agent_to_grid(grid_name, position, model)

        self.assertEqual(len(agent.environment_positions), 0)

    def test_move_agent_invalid_3d(self):
        model = Model(5)
        grid_name = "sampleGridN3D"

        ObjectGrid3D(grid_name, 20, 20, 20, model)

        agent = SimpleAgent()

        position = (5, 6, 7)

        agent.add_agent_to_grid(grid_name, position, model)

        position_b = (50, 55, 60)

        agent.move_agent(grid_name, position_b, model)

        self.assertEqual(agent.environment_positions[grid_name], position)
        self.assertEqual(model.environments[grid_name].grid[position].pop(),
                         agent)
