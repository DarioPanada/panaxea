import unittest

from panaxea.core.Model import Model
from tests.resources.SampleSteppables import AgentX, AgentY, AgentZ
from panaxea.toolkit.Toolkit import AgentSummary


class TestToolkit(unittest.TestCase):

    def test_agent_summary(self):
        model = Model(5)
        model.schedule.agents.add(AgentX())
        model.schedule.agents.add(AgentX())
        model.schedule.agents.add(AgentX())
        model.schedule.agents.add(AgentY())
        model.schedule.agents.add(AgentY())
        model.schedule.agents.add(AgentZ())

        # Important, also testing agentsToSchedule array
        model.schedule.agents_to_schedule.add(AgentX())

        ags = AgentSummary()
        summary = ags.step_epilogue(model)
        self.assertEqual(summary['AgentX'], 4)
        self.assertEqual(summary['AgentY'], 2)
        self.assertEqual(summary['AgentZ'], 1)


if __name__ == '__main__':
    unittest.main()
