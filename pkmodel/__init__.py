"""pkmodel is a Pharmokinetic modelling library.

It contains functionality for creating, solving, and visualising the solution
of Parmokinetic (PK) models

"""
# Import version info
from .version_info import VERSION_INT, VERSION  # noqa

# Import main classes

from .pk_model import PKModel
from .compartment import Compartment
from .functions import zeroth_order, first_order, dose_constant, dose_steady
from .pkanalysis import plot_solution