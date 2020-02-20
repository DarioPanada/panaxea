class Steppable(object):
    """
    Represents generic steppable object. Steppables represent entities which
    can be added to the schedule and whose
    logic is excuted once per epoch.

    Steppables implement a prologue, main and epilogue. All prologues for
    all steppables are executed first, followed
    by all mains followed by all epilogues.
    """

    def __init__(self):
        pass

    def step_prologue(self, model):
        """
        Placeholder to enforce that all steppables implement a stepPrologue
        method with the correct signature. Per se,
        this method does nothing but can be overridden by child classes.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule to which the
            agent belong is bound.
        """
        pass

    def step_main(self, model):
        """
        Placeholder to enforce that all steppables implement a stepMain
        method with the correct signature. Per se,
        this method does nothing but can be overridden by child classes.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule to which the
            agent belong is bound.
        """
        pass

    def step_epilogue(self, model):
        """
        Placeholder to enforce that all steppables implement a stepEpilogue
        method with the correct signature. Per se,
        this method does nothing but can be overridden by child classes.

        Parameters
        ----------
        model : Model
            The instance of the model to which the schedule to which the
            agent belong is bound.
        """
        pass


class Agent(Steppable):
    """
    An agent represents a self-contained unit in the simulation with a
    state, a beahaviour and which may interact with,
    be affected by and affect the environment and other agents. A simulation
    may have multiple agent classes.

    Examples of agent classes may include people, tissue cells, etc.
    """

    def __init__(self):
        # This is a dictionary mapping an environment name to a position.
        # This is so we don't have to do a search
        # on the environment grid each time we want to know our position. At
        # the same time, it's useful to also have
        # a grid of agents to quickly search neighbourhoods.
        self.environment_positions = dict()

    def add_agent_to_grid(self, environment_name, position, model):
        """
        Adds an agent to a position in a grid. This both updates the state
        of the grid (via API calls to the grid object)
        **and** the internal state of the agent.

        This does **not** check if the agent already exists in the grid. So,
        it potentially allows for the agent to be
        added to the same grid multiple times.

        This method does check whether a position is valid, and where that
        is not the case the agent is not added
        and a warning is printed to screen.

        Parameters
        ----------
        environment_name : string
            The name of the environment to which the agent should be added.
            This should match the name property
            in the environment object.
        position : tuple
            The position to which the agent will be added. This should be
            given as a tuple of two or three values,
            depending if this object grid is associated to a 2D or 3D
            environment.
        model : Model
            The instance of the model on which the simulation is based.
        """
        env = model.environments[environment_name]

        if env.valid_position(position):
            self.environment_positions[environment_name] = position

            env.add_agent(self, position)
        else:
            print("Invalid position %s on grid %s" % (
                str(position), environment_name))

    def move_agent(self, environment_name, position_new, model):
        """
        Moves an agent from a position to another in an environment.

        This both updates the state of the grid (via API calls to the grid
        object) **and** the internal state
        of the agent.

        This method does check whether a position is valid, and where that
        is not the case the agent is not moved
        and a warning is printed to screen.

        Parameters
        ----------
        environment_name : string
            The name of the environment to which the agent should be added.
            This should match the name property
            in the environment object.
        position_new : tuple
            The position to which the agent will be moved to. This should be
            given as a tuple of two or three values,
            depending if this object grid is associated to a 2D or 3D
            environment.
        model : Model
            The instance of the model on which the simulation is based.
        """
        env = model.environments[environment_name]

        if env.valid_position(position_new):
            position_old = self.environment_positions[environment_name]

            # Updating the agent's internal representation
            self.environment_positions[environment_name] = position_new

            # Asking the environment to update its internal representation
            env.move_agent(self, position_old, position_new)

    def remove_agent_from_grid(self, environment_name, model):
        """
        Removes an agent from an environment.

        This both updates the state of the grid (via API calls to the grid
        object) **and** the internal state
        of the agent.

        This method does not check if an agent exists in an environment,
        but if it doesn't the method is trivially
        void.

        Parameters
        ----------
        environment_name : string
            The name of the environment to which the agent should be added.
            This should match the name property
            in the environment object.
        model : Model
            The instance of the model on which the simulation is based.
        """
        env = model.environments[environment_name]
        position = self.environment_positions[environment_name]

        env.remove_agent(self, position)
        self.environment_positions[environment_name] = None

    def remove_agent(self, model):
        """
        Removes an agent from the simulation. This removes the agent all
        environments and from the schedule.

        In removing an agent from all environments, the internal state of
        the agent is also updated.

        In practice, the agent is not immediately removed from the schedule
        but is added to the list of agents to remove
        and will be removed at the following epcoh.

        Parameters
        ----------
        model : Model
            The instance of the model on which the simulation is based.
        """
        envs = self.environment_positions.keys()

        for env in envs:
            self.remove_agent_from_grid(env, model)

        model.schedule.agents_to_remove.add(self)


class Helper(Steppable):
    """
    A placeholder class to allow for helper steppables to have their own
    data-type.

    A helper allows to encapsulate logic that should be executed at each
    time-step, but which does not belong to any
    agent. Common examples could include functions to save text or graphics
    to an output file, record model properties,
    update environment properties, etc.

    This class does not provide methods or attributes, but allows for the
    "Helper" data-type to exist which is a bit
    more informative than simply having objects of 'Steppable' type.
    """

    def __init__(self):
        pass
