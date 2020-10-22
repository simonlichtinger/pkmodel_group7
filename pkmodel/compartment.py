# This holds the Compartment class


class Compartment:
    """Class to represent a pharmacological compartment, to used in generating
    a graph of compartments in the PKModel class. Functionality is to sum
    up the appropriate partial differential equation for this compartment.

    Fields:
        -   index:          Index of this Compartment within the PKModel
        -   volume:         Volume of this Compartment
        -   input_funcs:    List of all input functions leading into this compartment
        -   output_funcs:   List of all output function leading from this compartment

    Methods:
        -   __init__:           Initialise all fields of the class
        -   differential_eq:    Sum of inputs and outputs to arrive at RHS of dq_i/dt
    """

    def __init__(self, index: float, volume: float, in_func, out_func) -> None:
        """Method to initialise a new Compartment with some baseline functionality.

        :param index: Index of the Compartment within the PKModel
        :param volume: Volume of the Compartment to be used for PK modelling functionality.
        :param in_func: First input function the Compartment is set up with, eg. dosing function.
        :param out_func: First output function the Compartment is set up with, eg. circulation elimination.
        """
        self.input_funcs = [in_func] if in_func is not None else []
        self.output_funcs = [out_func] if out_func is not None else []
        self.index = index
        self.volume = volume

    def differential_eq(self, t: float, q: list) -> float:
        """Method to return the overall RHS of the
        differential equation dq_i / dt = differential_eq(t,q) for this Compartment.

        :param t: Time point
        :param q: Vector (list) of drug mass in all compartments.
        :returns: Value of the RHS of the compartment differential equation.
        """
        try:
            return sum([func(t, q) for func in self.input_funcs]) - sum(
                [func(t, q) for func in self.output_funcs]
            )
        except TypeError:
            raise TypeError("All inputs and outputs must be functions which take 2 arguments: time t and mass distribution vector q.")
