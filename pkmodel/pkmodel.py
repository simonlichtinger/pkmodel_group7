# This holds the PKModel class

from compartment import Compartment

#from template_functions import zeroth_order 
# This would be later, now just use some dummy functions to be able to implement
def zeroth_order(t: float, q: list, time_constant: float) -> float:
    return time_constant

def first_order(t: float, q: list, time_constant: float, input_index: int) -> float:
    return time_constant* q[input_index]


class PKModel:
    """ This is the docstring """
    def __init__(self) -> None:
        """ Very basic init, doesn't create any model -> need to create model by create_model or load_json."""
        self.compartments = []
        self.resolving_indices = dict()

    def create_model(self, name: str, volume: float, dosing_func = zeroth_order, dosing_time_constant = 1: float, elimination_func = first_order, elimination_time_constant = 1: float) -> None:
        """ Set up a basic one-compartment model, with a given compartment name. Dosing and elimination parameters
        are collected as keyword arguments.

        :param name:                        name of the compartment
        :param volume:                      volume of the compartment
        :param dosing_func:                 (optional) Specify the dosing function as input to the compartment. Default is zeroth order (constant). If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and concentration vector q arguments.
        :param dosing_time_constant:        (optional) Time constant to be used in the zeroth order default dosing function.
        :param elimination_func:            (optional) Specify the elimination function as output from the compartment. Default is first order (constant). If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and concentration vector q arguments.
        :param elimination_time_constant:   (optional) Time constant to be used in the first order default elimination function.
        """
        # Set up input and output functions with the given parameters
        in_func = lambda t, q: dosing_func(t, q, dosing_time_constant)
        out_func = lambda t, q: elimination_func(t, q, elimination_time_constant/volume, input_index = 0)

        # Create compartment and add index to the dictionary of indices by name
        resolving_indices[name] = 0
        compartments.append(Compartment(0, volume, in_func, out_func))