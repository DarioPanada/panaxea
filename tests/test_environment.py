import unittest

from panaxea.core.Environment import ObjectGrid2D, NumericalGrid2D, \
    ObjectGrid3D, NumericalGrid3D
from panaxea.core.Model import Model
from tests.resources.SampleSteppables import SimpleAgent, AgentX


class TestEnvironment(unittest.TestCase):

    # Tests for ObjectGrid2D

    def test_object_grid_2d_sample(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        grid_name = "sampleGridA"

        env = ObjectGrid2D(grid_name, xsize, ysize, model)

        self.assertEqual(env.xsize, xsize)
        self.assertEqual(env.ysize, ysize)

        self.assertEqual(env.name, grid_name)

        self.assertEqual(len(env.grid[(0, 0)]), 0)

        self.assertEqual(env, model.environments[grid_name])

    def test_object_grid_3d_sample(self):
        model = Model(5)

        xsize = 20
        ysize = 25
        zsize = 30
        grid_name = "sampleGrid3DA"

        env = ObjectGrid3D(grid_name, xsize, ysize, zsize, model)

        self.assertEqual(env.xsize, xsize)
        self.assertEqual(env.ysize, ysize)
        self.assertEqual(env.zsize, zsize)

        self.assertEqual(env.name, grid_name)

        self.assertEqual(len(env.grid[(0, 0, 0)]), 0)
        self.assertEqual(env, model.environments[grid_name])

    # Tests for NumericalGrid2D
    def test_numerical_grid_2d(self):
        model = Model(5)

        grid_name = "sampleGridC"

        xsize = 20
        ysize = 25

        env = NumericalGrid2D(grid_name, xsize, ysize, model)

        self.assertEqual(model.environments[grid_name], env)
        self.assertEqual(env.grid[(0, 0)], 0.0)

    def test_valid_position_2d(self):
        model = Model(5)

        grid_name = "sampleGridD"

        xsize = 20
        ysize = 25

        env = NumericalGrid2D(grid_name, xsize, ysize, model)

        self.assertTrue(env.valid_position((12, 12)))
        self.assertTrue(env.valid_position((0, 0)))
        self.assertFalse(env.valid_position((-1, -1)))
        self.assertFalse(env.valid_position((20, 25)))
        self.assertFalse(env.valid_position((20, 19)))
        self.assertFalse(env.valid_position((22, 23)))

    def test_full_2d_neighbourhood(self):
        model = Model(5)

        grid_name = "sampleGridD"

        xsize = 20
        ysize = 25

        env = NumericalGrid2D(grid_name, xsize, ysize, model)

        neigh = env.get_moore_neighbourhood((2, 3))

        expected_neigh = [
            (3, 2),
            (3, 3),
            (3, 4),
            (2, 2),
            (2, 4),
            (3, 2),
            (3, 3),
            (3, 4)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_partial_2d_neighbourhood_lower(self):
        model = Model(5)

        grid_name = "sampleGridE"

        xsize = 20
        ysize = 25

        env = NumericalGrid2D(grid_name, xsize, ysize, model)

        neigh = env.get_moore_neighbourhood((0, 0))

        expected_neigh = [
            (1, 0),
            (1, 1),
            (0, 1)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_partial_2d_neighbourhood_upper(self):
        model = Model(5)

        grid_name = "sampleGridF"

        xsize = 20
        ysize = 20

        env = NumericalGrid2D(grid_name, xsize, ysize, model)

        neigh = env.get_moore_neighbourhood((19, 19))

        expected_neigh = [
            (19, 18),
            (19, 18),
            (18, 19)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_get_most_populated_moore_neigh(self):
        model = Model(5)

        grid_name = "sampleGridG"

        env = ObjectGrid2D(grid_name, 50, 50, model)

        a = AgentX()
        b = AgentX()
        c = AgentX()

        max_pos = (20, 20)

        a.add_agent_to_grid(grid_name, max_pos, model)
        b.add_agent_to_grid(grid_name, max_pos, model)
        c.add_agent_to_grid(grid_name, (19, 20), model)

        self.assertEqual(env.get_most_populated_moore_neigh((19, 19)), max_pos)

    def test_get_most_populated_moore_neigh_edgecase(self):
        model = Model(5)

        grid_name = "sampleGridH"

        env = ObjectGrid2D(grid_name, 50, 50, model)
        self.assertEqual(env.get_most_populated_moore_neigh((100, 100)), None)

    def test_get_least_populated_moore_neigh_(self):
        model = Model(5)

        grid_name = "sampleGridI"

        env = ObjectGrid2D(grid_name, 50, 50, model)

        a = AgentX()
        b = AgentX()
        c = AgentX()
        d = AgentX()
        e = AgentX()
        f = AgentX()
        g = AgentX()

        a.add_agent_to_grid(grid_name, (19, 21), model)
        b.add_agent_to_grid(grid_name, (20, 21), model)
        c.add_agent_to_grid(grid_name, (21, 21), model)
        d.add_agent_to_grid(grid_name, (19, 20), model)
        e.add_agent_to_grid(grid_name, (21, 20), model)
        f.add_agent_to_grid(grid_name, (19, 19), model)
        g.add_agent_to_grid(grid_name, (20, 19), model)

        self.assertEqual(env.get_least_populated_moore_neigh((20, 20)),
                         (21, 19))

    def test_get_least_populated_moore_neigh_edgecase(self):
        model = Model(5)

        grid_name = "sampleGridJ"

        env = ObjectGrid2D(grid_name, 50, 50, model)
        self.assertEqual(env.get_least_populated_moore_neigh((100, 100)), None)

    # Tests for NumericalGrid3D
    def test_numerical_grid_3d(self):
        model = Model(5)

        grid_name = "sampleGridN"

        xsize = 20
        ysize = 25
        zsize = 30

        env = NumericalGrid3D(grid_name, xsize, ysize, zsize, model)

        self.assertEqual(model.environments[grid_name], env)
        self.assertEqual(env.grid[(0, 0, 0)], 0.0)

    def test_valid_position_3d(self):
        model = Model(5)

        grid_name = "sampleGridZ"

        xsize = 20
        ysize = 25
        zsize = 30

        env = NumericalGrid3D(grid_name, xsize, ysize, zsize, model)

        self.assertTrue(env.valid_position((12, 12, 12)))
        self.assertTrue(env.valid_position((0, 0, 0)))
        self.assertFalse(env.valid_position((-1, -1, -1)))
        self.assertFalse(env.valid_position((20, 25, 30)))
        self.assertFalse(env.valid_position((20, 19, 15)))
        self.assertFalse(env.valid_position((22, 23, 27)))
        self.assertFalse(env.valid_position((1, 1, 35)))

    def test_full_3d_neighbourhood(self):
        model = Model(5)

        grid_name = "sampleGridD"

        xsize = 20
        ysize = 25
        zsize = 30

        env = NumericalGrid3D(grid_name, xsize, ysize, zsize, model)

        neigh = env.get_moore_neighbourhood((2, 3, 4))

        expected_neigh = [
            (3, 4, 5),
            (3, 4, 3),
            (3, 4, 4),
            (3, 2, 5),
            (3, 2, 3),
            (3, 2, 4),
            (3, 3, 5),
            (3, 3, 3),
            (3, 3, 4),
            (1, 4, 5),
            (1, 4, 3),
            (1, 4, 4),
            (1, 2, 5),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 5),
            (1, 3, 3),
            (1, 3, 4),
            (2, 4, 5),
            (2, 4, 3),
            (2, 4, 4),
            (2, 2, 5),
            (2, 2, 3),
            (2, 2, 4),
            (2, 3, 5),
            (2, 3, 3)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_filtered_neighbourhood_upper_3d(self):
        model = Model(5)

        grid_name = "sampleGridD"

        xsize = 5
        ysize = 5
        zsize = 5

        env = NumericalGrid3D(grid_name, xsize, ysize, zsize, model)

        neigh = env.get_moore_neighbourhood((2, 3, 4))

        expected_neigh = [
            (3, 4, 3),
            (3, 4, 4),
            (3, 2, 3),
            (3, 2, 4),
            (3, 3, 3),
            (3, 3, 4),
            (1, 4, 3),
            (1, 4, 4),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 3),
            (1, 3, 4),
            (2, 4, 3),
            (2, 4, 4),
            (2, 2, 3),
            (2, 2, 4),
            (2, 3, 3)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_filtered_neighbourhood_lower_3d(self):
        model = Model(5)

        grid_name = "sampleGridD"

        xsize = 5
        ysize = 5
        zsize = 5

        env = NumericalGrid3D(grid_name, xsize, ysize, zsize, model)

        neigh = env.get_moore_neighbourhood((0, 0, 0))

        expected_neigh = [
            (1, 1, 1),
            (1, 1, 0),
            (1, 0, 1),
            (1, 0, 0),
            (0, 1, 1),
            (0, 1, 0),
            (0, 0, 1)
        ]

        self.assertEqual(len(neigh), len(expected_neigh))

        for en in expected_neigh:
            self.assertTrue(en in neigh,
                            "Expecting %s to be in neighbourhood but wasn't"
                            % str(
                                en))

    def test_get_most_populated_moore_neigh_3d(self):
        model = Model(5)
        env_name = "env"

        grid = ObjectGrid3D(env_name, 20, 20, 20, model)

        a = SimpleAgent()
        a.add_agent_to_grid(env_name, (17, 17, 17), model)

        self.assertEqual(grid.get_most_populated_moore_neigh((17, 16, 17)),
                         (17, 17, 17))

    def test_get_least_populated_moore_neigh_3d(self):
        model = Model(5)
        env_name = "env"

        grid = ObjectGrid3D(env_name, 20, 20, 20, model)

        neigh = grid.get_moore_neighbourhood((15, 15, 15))
        excluded_pos = neigh.pop()

        for n in neigh:
            a = SimpleAgent()
            a.add_agent_to_grid(env_name, n, model)

        self.assertEqual(grid.get_least_populated_moore_neigh((15, 15, 15)),
                         excluded_pos)

    def test_get_min_moore_neigh_2d(self):
        model = Model(5)

        grid = NumericalGrid2D("env", 10, 10, model)

        target_pos = (2, 2)
        to_exclude = (1, 2)

        neigh = grid.get_moore_neighbourhood(target_pos)

        for n in neigh:
            if n == to_exclude:
                continue

            grid.grid[(n[0], n[1])] = 5

        self.assertEqual(grid.get_least_in_neigh(target_pos), to_exclude)

    def test_get_min_moore_neigh_2d_edge(self):
        model = Model(5)

        grid = NumericalGrid2D("env", 10, 10, model)

        target_pos = (0, 0)
        to_exclude = (1, 1)

        neigh = grid.get_moore_neighbourhood(target_pos)

        for n in neigh:
            if n == to_exclude:
                continue

            grid.grid[(n[0], n[1])] = 5

        self.assertEqual(grid.get_least_in_neigh(target_pos), to_exclude)

    def test_get_max_moore_neigh_2d(self):
        model = Model(5)

        grid = NumericalGrid2D("env", 10, 10, model)

        target_pos = (2, 2)

        grid.grid[(1, 2)] = 3

        max_pos = (2, 1)

        grid.grid[(max_pos[0], max_pos[1])] = 5

        self.assertEqual(grid.get_max_in_neigh(target_pos), max_pos)

    def test_get_max_moore_neigh_2d_edge(self):
        model = Model(5)

        grid = NumericalGrid2D("env", 10, 10, model)

        target_pos = (0, 0)

        grid.grid[(1, 1)] = 3

        max_pos = (0, 1)

        grid.grid[(max_pos[0], max_pos[1])] = 5

        self.assertEqual(grid.get_max_in_neigh(target_pos), max_pos)

    def test_get_min_moore_neigh_3d(self):
        model = Model(5)

        grid = NumericalGrid3D("env", 10, 10, 10, model)

        target_pos = (2, 2, 2)
        to_exclude = (1, 2, 2)

        neigh = grid.get_moore_neighbourhood(target_pos)

        for n in neigh:
            if n == to_exclude:
                continue

            grid.grid[n] = 5

        self.assertEqual(grid.get_least_in_neigh(target_pos), to_exclude)

    def test_get_min_moore_neigh_3d_edge(self):
        model = Model(5)

        grid = NumericalGrid3D("env", 10, 10, 10, model)

        target_pos = (0, 0, 0)
        to_exclude = (1, 1, 1)

        neigh = grid.get_moore_neighbourhood(target_pos)

        for n in neigh:
            if n == to_exclude:
                continue

            grid.grid[n] = 5

        self.assertEqual(grid.get_least_in_neigh(target_pos), to_exclude)

    def test_get_max_moore_neigh_3d(self):
        model = Model(5)

        grid = NumericalGrid3D("env", 10, 10, 10, model)

        target_pos = (2, 2, 2)

        grid.grid[(1, 2, 2)] = 3

        max_pos = (2, 1, 1)

        grid.grid[(max_pos[0], max_pos[1], max_pos[2])] = 5

        self.assertEqual(grid.get_max_in_neigh(target_pos), max_pos)

    def test_get_max_moore_neigh_3d_edge(self):
        model = Model(5)

        grid = NumericalGrid3D("env", 10, 10, 10, model)

        target_pos = (0, 0, 0)

        grid.grid[(0, 0, 1)] = 3

        max_pos = (0, 1, 0)

        grid.grid[(max_pos[0], max_pos[1], max_pos[2])] = 5

        self.assertEqual(grid.get_max_in_neigh(target_pos), max_pos)


if __name__ == '__main__':
    unittest.main()
