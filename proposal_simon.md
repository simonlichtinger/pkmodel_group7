# class Compartment:

**index**: Index of the Compartment

**volume**: To be used for calculation of rate constants

**input_funcs**: List of functions which input into this Compartment

(**input_nodes**: List of node indices which are inputs)

**output_funcs**: List of functions which output from this Compartment

(**output_nodes**: List of node indices which are outputs)

**differential_eq(t,q)**: Returns the sum of all input and output functions

**__init__(*args)**: sets up the input and output funcs as required

=============

# class Network:

**resolving_indices**: Dict to hold trivial names for compartment indices

**compartments**: List of all Compartment objects

**add_parent(node, name, *args, shift_input=True)**: Adds a parent to a specified node, assigns the output of the new parent as the input of the child, and shifts the original input to the parent, if desired

**add_child(node, name, *args, shift_input=True)**: Adds a child to a specified node, assigns the input of the child from the output of the parent, and shifts the original output to the child, if desired

**add_sibling(node, name, *args)**: Creates a sibling to an existing node, by making a circle of inputs and outputs.

**add_connection(node1, node2, *args, exchange=False)**: This assigns input and output functions as needed to two nodes, to connect them -- if not created via the other add_* functions.

**differential_eq(t,q)**: Gathers the differential_eq's from moduels, which is easy because the LHS's are already separated, smth like ```[node.differential_eq(t,q) for node in copartments]```

**solve(initial_conditions,t_range)**: Uses scipy.integrate.solve_ivp to solve the equation given by differential_eq(t,q). Returns a scipy solution object.

**save_json** and **load_json** could be nice features to implement.

=============

# module PKAnalysis

This will hold several predefined model functions, like zeroth, first, etc order decays or equilibrium exchange. Will have the form ```func(t,q,*args)``` and will be stored internally via something like ```specific_func = lambda t,q: func(t,q,*args)```

**plot_solution(solution)**: Uses matplotlib to plot the output graph for a solution object.

(**plot_network(network)**: Would be nice feature to implement, to get a graphical representation of the network ...)

=============

# Advantages of the approach

* uses pythons flexible type system, to shorten the code by passing around functions directly, also ensuring flexibility
* can handle PK models of arbitrary type and complexity, while not being much more complicated to implement
* easily extensible, for instance by inheriting from Comparment, or defining one's own functions
