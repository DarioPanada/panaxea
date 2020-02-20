import copy
import time
from collections import Counter, defaultdict

from panaxea.core.Model import Model
from panaxea.core.Steppables import Helper

try:
    import cPickle as pickle
except ImportError:
    import pickle


class AgentSummary(Helper, object):
    """
    Helper class which, in the epilogue of each epoch, returns a summary of
    the count of agents belonging to each class
    considering the union of the schedule and agentsToSchedule.

    Attributes
    ----------
    recordEvery : int, optional
        Defines every how many epochs an agent summary is returned. Defaults
        to 1. (Ie: Every epoch)
    """

    def __init__(self, record_every=1):
        self.agentSummary = []
        self.recordEvery = record_every

    def step_epilogue(self, model):
        """
        Builds a summary of number of agents per agent class in the model.

        Parameters
        ----------
        model : Model
            An instance of the model on which the current simulation is based.

        Returns
        -------
        Counter
            A counter object where keys correspond to agent classes and
            values to agent counts.
        """
        if model.current_epoch % self.recordEvery == 0:
            c = Counter([a.__class__.__name__ for a in
                         model.schedule.agents.union(
                             model.schedule.agents_to_schedule)])
            self.agentSummary.append(c)

            return c


class ModelPickler(Helper, object):
    """
    At each epoch, outputs a serialized copy of the model in its current state.

    Attributes
    ----------
    outDir : string
        The directory where pickle files should be outputted. This should be
        specified as relative to the script
        from which the simulation is launched
    """

    def __init__(self, out_dir):
        self.outDir = out_dir

    def step_epilogue(self, model):
        """
        Creates and saves the pickle file.

        model : Model
            An instance of the model on which the current simulation is based.
        """
        with open("%s/epoch_%s.pickle" % (self.outDir, model.current_epoch),
                  "wb") as output_file:
            pickle.dump(model, output_file)


class ModelPicklerLite(Helper, object):
    """
    Creates a lighter version of the pickle allowing to include or exclude
    specific elements.

    Attributes
    ----------
    outDir : string
        The directory where pickle files should be outputted. This should be
        specified as relative to the script
        from which the simulation is launched
    prefix : string, optional
        A prefix that will be given to the name of each output file. Eg: For
        a prefix "my_model" a sample output
        file would be my_model_epoch_0.pickle Defaults to None
    pickleEvery: number, optional
        Determines the frequency of model serializing. A value of 1 will
        create one pickle per epoch, a value of 2
        will create a pickle every other epoch, etc. Defaults to 1.
    pickleSchedule : bool, optional
        If set to true, the schedule object will be included. This will also
        include all agents on the schedule.
        Defaults to false.
    pickleEnvs : bool, optional
        If set to true, all environment objects will be included. This also
        includes all agents in every environment.
        Defaults to false.
    """

    # If virtualPickle is set to true the modelLite will be returned rather
    # than pickled
    # pickleEvery means model with pickled every x epochs, defaults to 1
    def __init__(self, out_dir, prefix=None, pickle_every=1,
                 pickle_schedule=False, pickle_envs=False):
        self.out_dir = out_dir
        self.pickle_every = pickle_every
        self.prefix = prefix
        self.pickle_schedule = pickle_schedule
        self.pickle_envs = pickle_envs

    # It is important this is in the epilogue as we check for an exit flag
    # which is set by helpers in the prologue!
    def step_epilogue(self, model):
        """
        Makes a call to the pickleModel method. No special logic here,
        just delegating to the method.

        Parameters
        ----------
        model : Model
            An instance of the model on which the current simulation is based.
        """

        if model.current_epoch > 0 and (
                model.current_epoch % self.pickle_every == 0 or
                model.current_epoch == model.epochs - 1 or model.exit):
            self.pickle_model(model)

    def pickle_model(self, model):
        """
        Creates and serializes the pickleLight object based on previously
        defined properties.

        Parameters
        ----------
        model : Model
            An instance of the model on which the current simulation is based.
        """
        start = time.time()
        model_lite = Model(5)

        if self.pickleSchedule:
            model_lite.schedule.agents = model.schedule.agents.union(
                model.schedule.agents_to_schedule)

            for a in model_lite.schedule.agents:
                if a.__class__.__name__ == "CancerCell":
                    # Can't pickle functions
                    a.reactToDrug_ = None

        model_lite.schedule.helpers = [h for h in model.schedule.helpers if
                                       h.__class__.__name__ not in
                                       "ExitConditionWatcher"]

        if self.pickleEnvs:
            model_lite.environments = copy.deepcopy(model.environments)
            env_start = time.time()
            for k, v in model_lite.environments.iteritems():
                v.grid = dict(v.grid)
            env_end = time.time()
            print("Cloning environments took %s seconds" % str(
                env_end - env_start))

        model_lite.output = model.output

        model_lite.properties = model.properties
        # Can't pickle functions
        model_lite.properties["agents"]["cancerCells"][
            "drugReactFunction"] = None
        model_lite.current_epoch = model.current_epoch

        if self.prefix is None:
            target = "%s/epoch_%s.pickle" % (self.out_dir, model.current_epoch)
        else:
            target = "%s/%s_epoch_%s.pickle" % (
                self.out_dir, self.prefix, model.current_epoch)
        with open(target, "wb") as output_file:
            pickle.dump(model_lite, output_file)
        end = time.time()
        print("Pickler lite took %s seconds" % str(end - start))


def depickle_from_lite(picklePath):
    """
    Given a path to a pickle light file, recreates the corresponding object
    with all available properties

    This is **not** a helper and **should not be added to the schedule**. It
    is useful to recreate (partial)
    model objects.

    This model may or may not be runnable when recreated depending on
    whether all properties (schedule, environments...)
    were retained.

    Parameters
    ----------
    picklePath : string
        The path to the pickle file relative to where the function is being
        called from.

    Returns
    -------
    Model
        A (potentially incomplete) instance of a model derived from the
        pickle file.
    """
    with open(picklePath, 'rb') as f:
        model = pickle.load(f, encoding='latin1')

    # Handling both Python 2 and 3

    environment_keys = model.environments.keys()

    for environment_key in environment_keys:
        environment = model.environments[environment_key]

        if "ObjectGrid" in environment.__class__.__name__:
            model.environments[environment_key].grid = \
                defaultdict(set, environment.grid)
        else:
            model.environments[environment_key].grid = \
                defaultdict(int, environment.grid)
    return model
