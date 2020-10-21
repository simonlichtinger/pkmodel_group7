# This sets up unit tests to be run with pytest on compartment.py

import pytest

def test_simple_differential_eq():
    from ..compartment import Compartment
    test_compartment = Compartment(0, 1, lambda t,q: 1, lambda t,q: q[0])

    assert test_compartment.differential_eq(0,[0]) == 1
    assert test_compartment.differential_eq(0,[2]) == -1

def test_invalid_function_input():
    from ..compartment import Compartment

    test_compartment = Compartment(0,1, lambda t: 1,lambda t,q: q[0]) # Input has wrong number of arguments
    with pytest.raises(TypeError):
        test_compartment.differential_eq(0,[0])

    test_compartment = Compartment(0,1, "Not a function",lambda t,q: q[0])
    with pytest.raises(TypeError):
        test_compartment.differential_eq(0,[0])