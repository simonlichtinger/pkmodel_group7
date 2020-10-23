# This holds the PKModel class

from .compartment import Compartment
import scipy.integrate
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from .functions import first_order, dose_constant, dose_steady


class PKModel:
    """Class to represent the complete PKModel. The public methods presented handle building a network of compartments
    and connecting them with in/output functions. The differential equations for the network can then be solved using scipy.

    Fields:
        -   _resolving_indices:     Dictionary to map names of compartments to their indices in the list.
        -   _compartments:          List of all Compartment objects the model contains.
        -   _network_edges:         Keeps track of all newly generated network edges for the purpose of later drawing.
        -   _in_edge / _out_edge:   Keeps track of special -- potentially shifted -- in/out edges.

    Methods:
        -   create_model:           Set up a basic one-compartment model.
        -   add_parent:             Add an upstream/parent node to an existing node.
        -   add_parent:             Add a downstream/child node to an existing node.
        -   add_sibling:            Add a side-by-side/sibling node to an existing node, with an equilibrium in between.
        -   add_input:              Manually add an input function to a node.
        -   add_output:             Manually add an output function to a node.
        -   differential_eq:        The complete set of differential equations for all compartments.
        -   solve:                  Solve the ODEs for some initial conditions using the scipy module.

        -   __init__:               Basic initialisation, no model created.
        -   __add_new_index:        Utility method to handle insertion of a new node into the dictionary.
        -   _permute_list_indices:  Simple utility to permute two list indices.
        -   draw_network:           This uses networkx to draw a map of the model
    Properties:
        -   get_compartment_names:  Returns a list of all compartment names of the model, in order of their index.
    """

    def __init__(self) -> None:
        """ Very basic init, doesn't create any model -> need to create model by create_model or load_json."""
        self._compartments = []
        self._resolving_indices = dict()
        self._network_edges = []
        self._in_edge = None
        self._out_edge = None

    def create_model(
        self,
        name: str,
        volume: float,
        dosing_func=dose_constant,
        dosing_time_constant: float = 1,
        dosing_time_windows: list = [(0, 1), (2, 3)],
        elimination_func=first_order,
        elimination_time_constant: float = 1,
    ) -> None:
        """Set up a basic one-compartment model, with a given compartment name. Dosing and elimination parameters
        are collected as keyword arguments.

        :param name:                        name of the compartment
        :param volume:                      volume of the compartment
        :param dosing_func:                 (optional) Specify the dosing function as input to the compartment. Default is dose_constant. And alternative built-in function is dose_steady. If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and mass distribution vector q arguments.
        :param dosing_time_constant:        (optional) Time constant to be used in the zeroth order default dosing function. Default: 1
        :param dosing_time_windows:         (optional) If the dose_steady function is to be used: gives the time windows list. Default: [(0,1),(2,3)]
        :param elimination_func:            (optional) Specify the elimination function as output from the compartment. Default is first order. If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and mass distribution vector q arguments.
        :param elimination_time_constant:   (optional) Time constant to be used in the first order default elimination function (to be divided by the volume). Default: 1
        """
        # Set up input and output functions with the given parameters
        if dosing_func == dose_constant:
            in_func = lambda t, q: dosing_func(t, q, dosing_time_constant)
        elif dosing_func == dose_steady:
            in_func = lambda t, q: dosing_func(
                t, q, dosing_time_constant, dosing_time_windows
            )
        else:
            in_func = dosing_func
        if elimination_func == first_order:
            out_func = lambda t, q: elimination_func(
                t, q, elimination_time_constant / volume, 0
            )
        else:
            out_func = elimination_func

        # Create compartment and add index to the dictionary of indices by name
        self._resolving_indices[name] = 0
        self._compartments.append(Compartment(0, volume, in_func, out_func))

        # Add default in/out edges for network drawing
        self._in_edge = ("", name)
        self._out_edge = (name, "")

    def _add_new_index(self, new_name: str) -> int:
        """Determines the index to be used for a new node, and adds its name to the dictionary.

        :param new_name:    Name of the node to be created.
        :returns:           Index of the new node.
        """
        new_index = len(self._compartments)
        self._resolving_indices[new_name] = new_index
        return new_index

    def add_parent(
        self,
        node: str,
        new_name: str,
        volume: float,
        connection_function=first_order,
        connection_time_constant: float = 1,
        shift_input: bool = True,
    ) -> None:
        """Add a new compartment and place it upstream in the graph of an existing node. If needed, the first input function
        of the child is transferred to the new parent. The nodes are connected via a specified connection function.

        :param node:                        Name of the node to which the parent is to be attached.
        :param new_name:                    Name of the node to be created.
        :param volume:                      Volume of the new node.
        :param connection_function:         (optional) Specify the connecting function. Default is first order. If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and mass distribution vector q arguments.
        :param connection_time_constant:    (optional) Time constant for the first-order default connection function (to be divided by the volume). Default: 1
        :param shift_input:                 (optional) Decide whether the first input of the child should be transferred to the parent as input. Default is yes. Set to False, if the first input is not a dosing!
        """

        # Create the parent and the appropriate connection
        new_index = self._add_new_index(new_name)
        old_index = self._resolving_indices[node]

        if connection_function == first_order:
            connection = lambda t, q: connection_function(
                t, q, connection_time_constant / volume, new_index
            )
        else:
            connection = connection_function

        if (
            shift_input
        ):  # if needed, shift the childs first input to be the new parents input
            shifted_func = self._compartments[old_index].input_funcs[0]
            new_comp = Compartment(new_index, volume, shifted_func, connection)
            self._compartments[old_index].input_funcs[0] = connection
            self._in_edge = ("", new_name)
        else:
            # create new compartment, but don't do shifting (means that new parent input will be empty, unless filled with add_input).
            # The child will then get one more connection than before.

            new_comp = Compartment(new_index, volume, None, connection)
            self._compartments[old_index].input_funcs.append(connection)

        self._compartments.append(new_comp)

        # Add appropriate network edge
        self._network_edges.append((new_name, node))

    def _permute_list_indices(self, l: list, a: int, b: int) -> list:
        """ Little helper function to permute two indices of a list """
        l[a], l[b] = l[b], l[a]
        return l

    def add_child(
        self,
        node: str,
        new_name: str,
        volume: float,
        connection_function=first_order,
        connection_time_constant: float = 1,
        shift_output: bool = True,
        shift_correct_for_volume_change: bool = True,
    ) -> None:
        """Add a new compartment and place it downstream in the graph of an existing node. If needed, the first output function
        of the parent is transferred to the new child. The nodes are connected via a specified connection function.

        :param node:                        Name of the node to which the child is to be attached.
        :param new_name:                    Name of the node to be created.
        :param volume:                      Volume of the new node.
        :param connection_function:         (optional) Specify the connecting function. Default is first order. If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and mass distribution vector q arguments.
        :param connection_time_constant:    (optional) Time constant for the first-order default connection function (to be divided by the volume). Default: 1
        :param shift_output:                (optional) Decide whether the first output of the parent should be transferred to the child as output. Default is yes.
        :param shift_correct_for_volume_change:     (optional) This determines whether a correction for changed volume is made on shifting the input function. Default is yes. Set to False, if the first input is not a first-order process.
        """

        # Create the child and the appropriate connection
        new_index = self._add_new_index(new_name)
        old_index = self._resolving_indices[node]

        if connection_function == first_order:
            connection = lambda t, q: connection_function(
                t,
                q,
                connection_time_constant / self._compartments[old_index].volume,
                old_index,
            )
        else:
            connection = connection_function

        if shift_output:
            # if needed, shift the parents first output to be the new child's output
            # We will need to take care to permute the list indices of the differential equation, as to pass on on the correct mass distribution vector for shifting
            temp = self._compartments[old_index].output_funcs[
                0
            ]  # Needed because lambda functions are mutable in python ...
            if shift_correct_for_volume_change:
                # If necessary, adjust for the effect of the change in volume on the first order rate constant, assuming the time constant is the same self._permute_list_indices(q.copy(),new_index,old_index)
                shift_function = (
                    lambda t, q: temp(
                        t, self._permute_list_indices(q.copy(), new_index, old_index)
                    )
                    * self._compartments[old_index].volume
                    / volume
                )
            else:
                shift_function = lambda t, q: temp(
                    t, self._permute_list_indices(q.copy(), new_index, old_index)
                )
            new_comp = Compartment(new_index, volume, connection, shift_function)
            self._compartments[old_index].output_funcs[0] = connection
            self._out_edge = (new_name, "")
        else:
            # create new compartment, but don't do shifting (means that new child output will be empty, unless filled with add_output).
            # The parent will then get one more connection than before.
            new_comp = Compartment(new_index, volume, connection, None)
            self._compartments[old_index].output_funcs.append(connection)

        self._compartments.append(new_comp)

        # Add appropriate network edge
        self._network_edges.append((node, new_name))

    def add_sibling(
        self,
        node: str,
        new_name: str,
        volume: float,
        connection_function=first_order,
        connection_time_constant: float = 1,
    ) -> None:
        """Add a new compartment and place it to the side in the graph of an existing node,
        ie connected by in input <-> output equilibrium. The nodes are connected via a specified connection function.

        :param node:                        Name of the node to which the child is to be attached.
        :param new_name:                    Name of the node to be created.
        :param volume:                      Volume of the new node.
        :param connection_function:         (optional) Specify the connecting function. Default is first order. If a user-defined function is specified, it needs to have parameters already built-in, ie taking only time t and mass distribution vector q arguments.
        :param connection_time_constant:    (optional) Time constant for the first-order default connection function (to be divided by the volume). Default: 1
        """

        # Create the child and the appropriate connection
        new_index = self._add_new_index(new_name)
        old_index = self._resolving_indices[node]

        if (
            connection_function == first_order
        ):  # Create the connection functions in both directions! out = to the sibling, in = from the sibling
            connection_out = lambda t, q: connection_function(
                t,
                q,
                connection_time_constant / self._compartments[old_index].volume,
                old_index,
            )
            connection_in = lambda t, q: connection_function(
                t, q, connection_time_constant / volume, new_index
            )
        else:
            raise TypeError(
                "Connections between siblings need to be first order for equilibrium exchange! Consider adding inputs and outputs manually if you wish different behaviour."
            )

        # Add new compartment with appropriate in/out streams
        new_comp = Compartment(new_index, volume, connection_out, connection_in)
        # Add the reverse streams to the original nodes
        self._compartments[old_index].input_funcs.append(connection_in)
        self._compartments[old_index].output_funcs.append(connection_out)

        self._compartments.append(new_comp)

        # Add network double edge
        self._network_edges.append((node, new_name))
        self._network_edges.append((new_name, node))

    def add_input(self, node: str, in_func, label: str = "unk. input") -> None:
        """Add an input function to a specified node manually.

        :param node:    Name of node to which the input is to be added.
        :param in_func: Input function, needs to take two positional arguments, time t and mass distribution vector q.
        :param label:   (optional) Label to be used for input in graph drawing.
        """
        self._compartments[self._resolving_indices[node]].input_funcs.append(in_func)
        self._network_edges.append((label, node))

    def add_output(self, node: str, out_func, label: str = "unk. output") -> None:
        """Add an output function to a specified node manually.

        :param node:        Name of node to which the input is to be added.
        :param out_func:    Output function, needs to take two positional arguments, time t and mass distribution vector q.
        :param label:       (optional) Label to be used for output in graph drawing.
        """
        self._compartments[self._resolving_indices[node]].output_funcs.append(out_func)
        self._network_edges.append((node, label))

    def differential_eq(self, t: float, q: list) -> list:
        """Get the vector (list) of differential equation right hand sides, ie dq/dt, for all compartments.

        :param t: Time point
        :param q: Vector (list) of drug mass in all compartments.
        :returns: List of the RHS values of the compartment differential equations.
        """
        assert len(q) == len(
            self._compartments
        ), "Need to have vector of the same dimensions as the number of compartments"
        return [comp.differential_eq(t, q) for comp in self._compartments]

    def solve(self, t_eval: np.ndarray, q0: np.ndarray):
        """Solve the PKModel for a set of initial conditions over a series of time points.

        :param t_eval:  Array of time-points of interest
        :param q0:      Initial conditions of mass distribution in compartments. This must have the correct length of the number of compartments present.
        """
        assert len(q0) == len(
            self._compartments
        ), "Initial conditions must be of the same dimensions as the number of compartments."
        return scipy.integrate.solve_ivp(
            fun=self.differential_eq,
            t_span=[t_eval[0], t_eval[-1]],
            y0=q0,
            t_eval=t_eval,
        )

    @property
    def get_compartment_names(self) -> list:
        """Get names of compartments currently stored in the model.

        :returns:   list of all keys of the dictionary holding the names of compartments.
        """
        return list(self._resolving_indices.keys())

    def draw_network(self, testing=False, layout=nx.spectral_layout) -> None:
        """Uses networkx to plot a graphical outline of the generated network.

        :param testing: (optional) When testing in continuous integration, can't plot.
        :param layout:  (optional) Provide details of wanted networkx layout.
        """
        G = nx.DiGraph()

        # Collect previously defined edges
        for edge in self._network_edges:
            G.add_edge(edge[0], edge[1])
        G.add_edge(self._in_edge[0], self._in_edge[1])
        G.add_edge(self._out_edge[0], self._out_edge[1])

        pos = layout(G)  # positions for all nodes

        nx.draw_networkx_nodes(G, pos, node_size=0)
        nx.draw_networkx_edges(
            G,
            pos,
            width=2,
            arrowstyle="->",
            arrowsize=20,
            min_source_margin=30,
            min_target_margin=30,
            connectionstyle="arc3,rad=0.2",
        )

        nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

        if not testing:
            plt.show()
