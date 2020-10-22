# This sets up unit tests to be run with pytest on compartment.py

import pytest
import scipy.integrate
import numpy as np


def test_base_model():
    from pkmodel.pkmodel import PKModel

    test_model = PKModel()
    test_model.create_model(
        "central", 1
    )  # Testing for just the main initial compartment functionality

    assert test_model.differential_eq(0, [1]) == [0]
    assert test_model.differential_eq(0, [2]) == [-1]
    assert test_model.differential_eq(0, [0]) == [1]

    test_model = PKModel()
    test_model.create_model("central", 1, dosing_time_constant=2)

    assert test_model.differential_eq(0, [1]) == [1]

    with pytest.raises(
        AssertionError
    ):  # Shouldn't work because only one compartment but the given list is of length 2
        test_model.differential_eq(0, [1, 2])


def test_complex_network():  # create a model with non-standard values, and parent, child and sibling
    from pkmodel.pkmodel import PKModel

    test_model = PKModel()
    test_model.create_model(
        "main", 1, dosing_time_constant=2, elimination_time_constant=2
    )
    test_model.add_parent("main", "parent", 1, connection_time_constant=0.5)
    test_model.add_child("main", "child", 1 / 3, connection_time_constant=4)
    test_model.add_sibling("main", "sibling", 0.5, connection_time_constant=3)

    assert test_model.differential_eq(0, [1, 2, 3, 4]) == [18, 1, -14, -21]


def util1(t, q):
    return t


def util2(t, q):
    return (t ** 2) * q[0]


def test_custom_functions():  # create a simple model, but use all non-standard functions, and create extra in/outputs
    from pkmodel.pkmodel import PKModel

    test_model = PKModel()
    test_model.create_model("main", 1, dosing_func=util1, elimination_func=util2)

    assert test_model.differential_eq(0, [1]) == [0]
    assert test_model.differential_eq(2, [1]) == [-2]

    test_model.add_input("main", lambda t, q: 5)
    test_model.add_output("main", lambda t, q: t)

    assert test_model.differential_eq(0, [1]) == [5]
    assert test_model.differential_eq(2, [1]) == [1]


def prototype_model_1():
    t_eval = np.linspace(0, 1, 1000)
    y0 = np.array([0.0, 0.0])
    model1_args = {
        "name": "model1",
        "Q_p1": 1.0,
        "V_c": 1.0,
        "V_p1": 1.0,
        "CL": 1.0,
        "X": 1.0,
    }
    args = [
        model1_args["Q_p1"],
        model1_args["V_c"],
        model1_args["V_p1"],
        model1_args["CL"],
        model1_args["X"],
    ]
    return scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs(t, y, *args),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0,
        t_eval=t_eval,
    )


def dose(t, X):
    return X


def rhs(t, y, Q_p1, V_c, V_p1, CL, X):
    q_c, q_p1 = y
    transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
    dqc_dt = dose(t, X) - q_c / V_c * CL - transition
    dqp1_dt = transition
    return [dqc_dt, dqp1_dt]


def test_against_prototype():  # Test against model 1 of the prototype
    from pkmodel.pkmodel import PKModel

    test_model = PKModel()
    test_model.create_model("main", 1)
    test_model.add_sibling("main", "peripheral", 1)

    proto_out = prototype_model_1()
    model_out = test_model.solve(np.linspace(0, 1, 1000), np.array([0.0, 0.0]))

    assert proto_out.y.all() == model_out.y.all()
