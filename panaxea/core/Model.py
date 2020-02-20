import os
import sys
import time
from collections import defaultdict

from panaxea.core.Schedule import Schedule


class Model(object):
    """
        Initializes a model object. The model object is the primary
        component of each simulation, holding the schedule,
        the environments, model properties, and the current progress in the
        simulation.

        Essentially, the model holds a snapshot of the simulation world at
        any point in progress.

        Attributes
        ----------
        epochs : int
            The number of epochs the simulation should run for.
        verbose : bool, optional
            If set to true, output is sent to standard output. If set to
            false, output (Ie: print statements) is
            disabled. Defaults to true.
        properties: dict, optional
            Specifies a dictionary of property values. This can follow any
            format he developers need and should be
            adapted to the simulation's needs. Defaults to an empty dictionary.
    """

    def __init__(self, epochs, verbose=True, properties=dict()):
        self.epochs = epochs
        self.schedule = Schedule()
        self.environments = dict()
        self.verbose = verbose
        self.current_epoch = 0
        self.properties = properties
        self.exit = False

        self.output = defaultdict(dict)

        # Changing sys.stdout messes with unittests, so we will not do it
        # running from a test
        if not self.verbose and "unittest" not in sys.modules:
            sys.stdout = os.devnull

    def run(self):
        """
        Runs the simulation for the number of epochs configured or until an
        the exit flag is set to true.

        Note that the state of the schedule, environments etc. will result
        altered after the model runs. If you
        wish to run the same model multiple times, you should first copy the
        original
        instance to a backup variable.
        """

        epochs_time = []

        for i in range(0, self.epochs):

            if self.exit:
                print("Exit flag set to true, finishing at epoch %s" % str(
                    self.current_epoch))
                break

            self.current_epoch = i
            start_time = time.time()
            print("Epoch %s" % i)

            self.schedule.step_schedule(self)
            time_taken = time.time() - start_time
            print("Epoch took %s seconds" % time_taken)
            epochs_time.append(time_taken)

        print("Total time %s" % str(sum(epochs_time)))

        if "unittest" not in sys.modules:
            sys.stdout = sys.__stdout__
