import unittest

from panaxea.core.Model import Model
from tests.resources.SampleSteppables import SampleAgent, SampleHelper


class TestSchedule(unittest.TestCase):

    def test_schedule(self):
        model = Model(5)

        agent = SampleAgent()

        model.schedule.agents_to_schedule.add(agent)

        self.assertEqual(1, len(model.schedule.agents_to_schedule))
        model.schedule.step_schedule(model)

        self.assertEqual(1, len(model.schedule.agents))
        self.assertEqual(0, len(model.schedule.agents_to_schedule))

        self.assertEqual(agent.a, 1)
        self.assertEqual(agent.b, 3)
        self.assertEqual(agent.c, 5)

        agentB = SampleAgent()

        model.schedule.agents_to_schedule.add(agentB)

        self.assertEqual(1, len(model.schedule.agents))
        self.assertEqual(1, len(model.schedule.agents_to_schedule))

        model.schedule.step_schedule(model)

        self.assertEqual(2, len(model.schedule.agents))
        self.assertEqual(0, len(model.schedule.agents_to_schedule))

        self.assertEqual(agent.a, 2)
        self.assertEqual(agent.b, 5)
        self.assertEqual(agent.c, 8)

        self.assertEqual(agentB.a, 1)
        self.assertEqual(agentB.b, 3)
        self.assertEqual(agentB.c, 5)

        model.schedule.agents_to_remove.add(agentB)
        model.schedule.step_schedule(model)

        self.assertEqual(1, len(model.schedule.agents))
        self.assertEqual(0, len(model.schedule.agents_to_remove))

    def test_agents_and_helpers(self):
        model = Model(5)

        agent = SampleAgent()
        helper = SampleHelper()

        model.schedule.agents_to_schedule.add(agent)

        self.assertEqual(0, len(model.schedule.agents))

        model.schedule.helpers.append(helper)

        self.assertEqual(1, len(model.schedule.helpers))

        model.schedule.step_schedule(model)
        self.assertEqual(1, len(model.schedule.agents))
        self.assertEqual(0, len(model.schedule.agents_to_schedule))

        self.assertEqual(agent.a, 1)
        self.assertEqual(agent.b, 3)
        self.assertEqual(agent.c, 5)

        self.assertEqual(helper.x, 10)
        self.assertEqual(helper.y, 11)
        self.assertEqual(helper.z, 12)

    def test_agent_setup(self):
        agent = SampleAgent()

        self.assertEqual(0, len(agent.environment_positions))
        agent.environment_positions["a"] = "b"
        self.assertEqual("b", agent.environment_positions["a"])


if __name__ == '__main__':
    unittest.main()
