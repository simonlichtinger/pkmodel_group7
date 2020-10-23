"""pkmodel is a pharmacokinetic modelling library.

It contains functionality for creating, solving, and visualising the solution
of pharmacokinetic (PK) models.

A quick tutorial for usage can be found on https://github.com/simonlichtinger/pkmodel_group7/TUTORIAL.md

"""
# Import version info
from .version_info import VERSION_INT, VERSION  # noqa

# Import main classes

from .pk_model import PKModel
from .compartment import Compartment
from .functions import zeroth_order, first_order, dose_constant, dose_steady
from .pkanalysis import plot_solution
