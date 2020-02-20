class Schedule(object):
    """
    Holds all simulation steppables and provides methods to progress
    simulation epochs.

    Agents should be added to *agentsToSchedule* and not to *agents*,
    they will then be copied to the schedule
    before the start of the next epoch.

    Similarly, agents which are to be removed should be added ot
    *agentsToRemove* and will be removed before the start
    of the next epoch.

    The list *agents* should not be accessed directly.

    The list *helpers* should be set during simulation setup.
    """

    def __init__(self):
        self.agents = set([])
        self.helpers = []
        self.agents_to_schedule = set([])
        self.agents_to_remove = set([])

    def step_schedule(self, model):
        """
        Adds and removes agents from the schedule as appropriate and
        executes all step methods of
        agents and helpers as appropriate.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule is bound.
        """

        self.agents = self.agents - self.agents_to_remove
        self.agents = self.agents | self.agents_to_schedule

        self.agents_to_schedule = set([])
        self.agents_to_remove = set([])

        print("I am stepping %s agents" % self.agents.__len__())

        self.step_prologues(model)
        self.step_mains(model)
        self.step_epilogues(model)

    def step_prologues(self, model):
        """
        Executes the StepPrologue method of all helpers first and all agents
        after.

        It is unlikely that this method would be called directly, but rather
        would be called as part of
        StepSchedule.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule is bound.
        """
        for h in self.helpers:
            h.step_prologue(model)

        for a in self.agents:
            a.step_prologue(model)

    def step_mains(self, model):
        """
        Executes the StepMan method of all helpers first and all agents after.

        It is unlikely that this method would be called directly, but rather
        would be called as part of
        StepSchedule.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule is bound.
        """
        for h in self.helpers:
            h.step_main(model)

        for a in self.agents:
            a.step_main(model)

    def step_epilogues(self, model):
        """
        Executes the StepEpilogue method of all helpers first and all agents
        after.

        It is unlikely that this method would be called directly, but rather
        would be called as part of
        StepSchedule.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule is bound.
        """
        for h in self.helpers:
            h.step_epilogue(model)

        for a in self.agents:
            a.step_epilogue(model)
