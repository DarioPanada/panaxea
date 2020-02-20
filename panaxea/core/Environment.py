from collections import defaultdict
from random import shuffle


class Environment(object):
    """
    Initializes a generic environment instance. Assigns the name and binds
    it to the model instance.

    This class would **not** be instantiated itself. It would be extended by
    a concrete environment extension.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, model):
        self.name = name
        model.environments[name] = self


class Grid3D(Environment, object):
    """
    Initializes a 3D Grid object. Assigns the name, size and binds it to a
    model instance.

    This class would **not** be instantiated itself as it lacks any concrete
    extension of the underlying
    grid. Rather, it is used to check whether  position in the grid is valid
    and provide moore neighbourhoods
    and additional information based on the geometry of a 3D grid.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    zsize : int
        The number of positions along the z-axis. In other words, the depth
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, zsize, model):
        super(Grid3D, self).__init__(name, model)
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize

    def valid_position(self, position):
        """
        Checks whether a coordinate is valid with regards to the size of the
        grid instance.

        Checks if none of the coordinate values are negative or out of bounds.

        Parameters
        ----------
        position : tuple
            A tuple consisting of exactly three element, each of them being
            an integer.

        Returns
        -------
        bool
            True if the position is a valid one, false otherwise.
        """
        return self.xsize > position[0] >= 0 and self.ysize > position[
            1] >= 0 and self.zsize > position[2] >= 0

    def get_moore_neighbourhood(self, position, shuffle_neigh=True):
        """
        Returns a list of moore neighbours for a given position.

        A moore neighbourhood is intended as all positions immediately
        adjacent to a target one.

        Parameters
        ----------
        position : tuple
            A tuple consisting of exactly three element, each of them being
            an integer.
        shuffle_neigh : bool
            Optional, if set to true the list of neighbours will be shuffled
            and returned in a random order.

        Returns
        -------
        list
            A list of moore neighbours
        """
        neigh = [
            (position[0] + 1, position[1] + 1, position[2] + 1),
            (position[0] + 1, position[1] + 1, position[2] - 1),
            (position[0] + 1, position[1] + 1, position[2]),
            (position[0] + 1, position[1] - 1, position[2] + 1),
            (position[0] + 1, position[1] - 1, position[2] - 1),
            (position[0] + 1, position[1] - 1, position[2]),
            (position[0] + 1, position[1], position[2] + 1),
            (position[0] + 1, position[1], position[2] - 1),
            (position[0] + 1, position[1], position[2]),
            (position[0], position[1] + 1, position[2] + 1),
            (position[0], position[1] + 1, position[2] - 1),
            (position[0], position[1] + 1, position[2]),
            (position[0], position[1] - 1, position[2] + 1),
            (position[0], position[1] - 1, position[2] - 1),
            (position[0], position[1] - 1, position[2]),
            (position[0], position[1], position[2] + 1),
            (position[0], position[1], position[2] - 1),
            (position[0] - 1, position[1] + 1, position[2] + 1),
            (position[0] - 1, position[1] + 1, position[2] - 1),
            (position[0] - 1, position[1] + 1, position[2]),
            (position[0] - 1, position[1] - 1, position[2] + 1),
            (position[0] - 1, position[1] - 1, position[2] - 1),
            (position[0] - 1, position[1] - 1, position[2]),
            (position[0] - 1, position[1], position[2] + 1),
            (position[0] - 1, position[1], position[2] - 1),
            (position[0] - 1, position[1], position[2]),
        ]

        neigh = [n for n in neigh if self.valid_position(n)]

        if shuffle_neigh:
            shuffle(neigh)

        return neigh


class Grid2D(Environment, object):
    """
    Initializes a 2D Grid object. Assigns the name, size and binds it to a
    model instance.

    This class would **not** be instantiated itself as it lacks any concrete
    extension of the underlying
    grid. Rather, it is used to check whether  position in the grid is valid
    and provide moore neighbourhoods
    and additional information based on the geometry of a 2D grid.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, model):
        super(Grid2D, self).__init__(name, model)
        self.xsize = xsize
        self.ysize = ysize

    def valid_position(self, position):
        """
        Checks whether a coordinate is valid with regards to the size of the
        grid instance.

        Checks if none of the coordinate values are negative or out of bounds.

        Parameters
        ----------
        position : tuple
            A tuple consisting of exactly two element, each of them being an
            integer.

        Returns
        -------
        bool
            True if the position is a valid one, false otherwise.
        """
        return self.xsize > position[0] >= 0 and self.ysize > position[1] >= 0

    def get_moore_neighbourhood(self, position, shuffle_neigh=True):
        """
        Returns a list of moore neighbours for a given position.

        A moore neighbourhood is intended as all positions immediately
        adjacent to a target one.

        Parameters
        ----------
        position : tuple
            A tuple consisting of exactly two element, each of them being an
            integer.
        shuffle_neigh : bool
            Optional, if set to true the list of neighbours will be shuffled
            and returned in a random order.

        Returns
        -------
        list
            A list of moore neighbours
        """
        neigh = [
            (position[0] + 1, position[1] - 1),
            (position[0] + 1, position[1]),
            (position[0] + 1, position[1] + 1),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1),
            (position[0] - 1, position[1] - 1),
            (position[0] - 1, position[1]),
            (position[0] - 1, position[1] + 1),
        ]

        neigh = [n for n in neigh if self.valid_position(n)]

        if shuffle_neigh:
            shuffle(neigh)

        return neigh


class ObjectGrid(object):
    """
    Initializes an ObjectGrid. Object grids at each position hold
    collections of objects. Most likely these would be
    instances of agents.

    This class provides common methods to and, move and remove agents from
    the grid. It also exposes methods to get
    agent densities at various positions.

    This class would **not** be itself instantiated, but would be extended
    by another class that would implement it.
    """

    def __init__(self):
        self.grid = defaultdict(set)

    def move_agent(self, agent, position_old, position_new):
        """
        Moves an agent from a grid position to another grid position.

        This class does *not* update the internal state of the agent. So,
        if the agent also keeps its own record
        of its position in the grid, this should be updated separately.

        It is up to the developer to check that the old position did indeed
        contain the agent. If an invalid position
        is provided as a new position, the agent will not be moved.

        Positions should be given as tuples of two or three values,
        depending if this object grid is associated
        to a 2D or 3D environment.

        Parameters
        ----------
        agent : Agent
            The instance of the agent we wish to update.
        position_old : tuple
            The old position of the agent.
        position_new : tuple
            The new position of the agent.
        """
        if self.valid_position(position_new):
            self.grid[position_old].remove(agent)
            self.grid[position_new].add(agent)

    def remove_agent(self, agent, position):
        """
        Removes an agent from a position.

        This class does *not* update the internal state of the agent. So,
        if the agent also keeps its own record
        of its position in the grid, this should be updated separately.

        Positions should be given as tuples of two or three values,
        depending if this object grid is associated
        to a 2D or 3D environment.

        Parameters
        ----------
        agent : Agent
            The instance of the agent we wish to update.
        position: tuple
            The position from which we wish to remove the agent.
        """
        self.grid[position].remove(agent)

    def get_most_populated_moore_neigh(self, position):
        """
        Gets the coordinates of the moore neighbour with the most agents. If
        multiple neighbours meet the criteria,
        any may be returned.

        A moore neighbourhood is defined as all positions immediately
        adjacent the one we are searching. It does not
        include the target position itself.

        Positions should be given and are returned as tuples of two or three
        values,
        depending if this object grid is associated to a 2D or 3D environment.

        Parameters
        ----------
        position: tuple
            The position whose neighbourhood we wish to search.

        Returns
        -------
        tuple
            The moore position with the highest number of agents.
        """

        neigh = self.get_moore_neighbourhood(position)

        if len(neigh) == 0:
            return None

        shuffle(neigh)
        max_pop = 0
        most_populated = neigh[0]

        for n in neigh:
            pop = self.grid[n].__len__()

            if pop > max_pop:
                max_pop = pop
                most_populated = n

        return most_populated

    def get_least_populated_moore_neigh(self, position):
        """
        Gets the coordinates of the moore neighbour with the fewest agents.
        If multiple neighbours meet the criteria,
        any may be returned.

        A moore neighbourhood is defined as all positions immediately
        adjacent the one we are searching. It does not
        include the target position itself.

        Positions should be given and are returned as tuples of two or three
        values,
        depending if this object grid is associated to a 2D or 3D environment.

        Parameters
        ----------
        position: tuple
            The position whose neighbourhood we wish to search.

        Returns
        -------
        tuple
            The moore position with the fewest number of agents.
        """
        neigh = self.get_moore_neighbourhood(position)

        if len(neigh) == 0:
            return None

        n = neigh[0]

        shuffle(neigh)
        min_pop = (self.grid[n]).__len__()
        min_populated = n

        for n in neigh:
            pop = (self.grid[n]).__len__()

            if int(pop) < min_pop:
                min_pop = pop
                min_populated = n

        return min_populated

    def add_agent(self, agent, position):
        """
        Adds an agent to a position in the environment.

        This does *not* check if an agent already exists at another
        position. This should be checked separately.

        This class does *not* update the internal state of the agent. So,
        if the agent also keeps its own record
        of its position in the grid, this should be updated separately.

        If an invalid position is provided, then the agent will not be added.

        Parameters
        ----------
        agent : Agent
            The instance of the agent we wish to update.
        position: tuple
            The position to which we wish to add the agent.
        """
        if self.valid_position(position):
            self.grid[position].add(agent)


class ObjectGrid3D(Grid3D, ObjectGrid, object):
    """
    Instantiates a 3D Object Grid. This extends Grid3D and ObjectGrid,
    allowing to place objects in a three-dimensional
    grid exposing all methods offered by the aforementioned classes.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    zsize : int
        The number of positions along the z-axis. In other words, the depth
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, zsize, model):
        Grid3D.__init__(self, name, xsize, ysize, zsize, model)
        ObjectGrid.__init__(self)


class ObjectGrid2D(Grid2D, ObjectGrid, object):
    """
    Instantiates a 2D Object Grid. This extends Grid2D and ObjectGrid,
    allowing to place objects in a twp-dimensional
    grid exposing all methods offered by the aforementioned classes.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, model):
        Grid2D.__init__(self, name, xsize, ysize, model)
        ObjectGrid.__init__(self)


class NumericalGrid(object):
    """
    Initializes a NumericalGrid object. A NumericalGrid holds a single
    number value at each position.

    This class exposes methods to explore a position's neighbourhood.

    This class would **not** be itself instantiated, but would be extended
    by another class that would implement it.
    """

    def __init__(self):
        self.grid = defaultdict(int)

    def get_max_in_neigh(self, position):
        """
        Gets the coordinates of the moore neighbour with the largest value.
        If multiple neighbours meet the criteria,
        any may be returned.

        A moore neighbourhood is defined as all positions immediately
        adjacent the one we are searching. It does not
        include the target position itself.

        Positions should be given and are returned as tuples of two or three
        values,
        depending if this object grid is associated to a 2D or 3D environment.

        Parameters
        ----------
        position: tuple
            The position whose neighbourhood we wish to search.

        Returns
        -------
        tuple
            The moore position with the largest value.
        """
        neigh = self.get_moore_neighbourhood(position)

        max_pos = neigh[0]
        max_value = 0

        for n in neigh:
            valAtPos = self.grid[n]
            if valAtPos > max_value:
                max_value = valAtPos
                max_pos = n

        return max_pos

    def get_least_in_neigh(self, position):
        """
        Gets the coordinates of the moore neighbour with the smallest value.
        If multiple neighbours meet the criteria,
        any may be returned.

        A moore neighbourhood is defined as all positions immediately
        adjacent the one we are searching. It does not
        include the target position itself.

        Positions should be given and are returned as tuples of two or three
        values,
        depending if this object grid is associated to a 2D or 3D environment.

        Parameters
        ----------
        position: tuple
            The position whose neighbourhood we wish to search.

        Returns
        -------
        tuple
            The moore position with the smallest value.
        """
        neigh = self.get_moore_neighbourhood(position)

        min_pos = neigh[0]
        min_value = self.grid[neigh[0]]

        for n in neigh:
            valAtPos = self.grid[n]
            if valAtPos < min_value:
                min_value = valAtPos
                min_pos = n

        return min_pos


class NumericalGrid2D(Grid2D, NumericalGrid, object):
    """
    Instantiates a 2D Numerical Grid. This extends Grid2D and NumericalGrid,
    allowing to store values in a
    two-dimensional grid exposing all methods offered by the aforementioned
    classes.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, model):
        Grid2D.__init__(self, name, xsize, ysize, model)
        NumericalGrid.__init__(self)


class NumericalGrid3D(Grid3D, NumericalGrid, object):
    """
    Instantiates a 3D Numerical Grid. This extends Grid3D and NumericalGrid,
    allowing to store values in a
    three-dimensional grid exposing all methods offered by the
    aforementioned classes.

    Attributes
    ----------
    name : string
        The name of the environment, this will be used when referring to it
        throughout the code. (Eg: AgentEnv,
        OxygenEnv, etc.)
    xsize : int
        The number of positions along the x-axis. In other words, the width
        of the environment.
    ysize : int
        The number of positions along the y-axis. In other words, the height
        of the environment.
    model : model
        The instance of the model class to which the environment will be
        attached.
    """

    def __init__(self, name, xsize, ysize, zsize, model):
        Grid3D.__init__(self, name, xsize, ysize, zsize, model)
        NumericalGrid.__init__(self)
