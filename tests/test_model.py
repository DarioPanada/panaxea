import unittest

from panaxea.core.Model import Model
from tests.resources.SampleSteppables import SimpleAgent, SimpleHelper


class TestModel(unittest.TestCase):

    def test_model_epochs(self):
        model = Model(5)
        self.assertEqual(model.epochs, 5)

    def test_simple_model(self):
        model = Model(5)

        agent = SimpleAgent()

        model.schedule.agents.add(agent)

        model.run()

        self.assertEqual(model.schedule.agents.pop().a, 5)

    def test_model_with_agent_and_helper(self):
        # Testing with a helper that changes the state of an agent
        model = Model(5)
        agent = SimpleAgent()
        helper = SimpleHelper()
        model.schedule.agents.add(agent)
        model.schedule.helpers.append(helper)
        model.run()

        self.assertEqual(model.schedule.agents.pop().a, 62)

    def test_get_epochs(self):
        model = Model(5)
        self.assertEqual(0, model.current_epoch)
        model.run()
        self.assertEqual(4, model.current_epoch)

    def test_model_properties(self):
        model = Model(5)
        model.properties['a'] = 'b'
        self.assertEqual(model.properties['a'], 'b')


if __name__ == '__main__':
    unittest.main()
