from pkmodel.pkmodel import PKModel
import matplotlib.pyplot as plt
import numpy as np
from pkmodel.pkanalysis import plot_solution

test_model = PKModel()
test_model.create_model("main", 1, dosing_time_constant=1, elimination_time_constant=1)
test_model.add_parent("main", "precompartment", 1, connection_time_constant=6)
test_model.add_sibling("main", "peripheral", 1, connection_time_constant=2)
sol = test_model.solve(
    np.linspace(0, 10, 10000),
    np.array(
        [
            0.0,
            0.0,
            0.0,
        ]
    ),
)
# Model 2 --- It appears as tho the three compartment model has not been added in
# There is not sufficient info in Scipy.integrate file to allow model graphical presentation to be model presentable at the moment
# Therefore the graph being produced is only one type for both models
# It is not cleare if the allocated comparments are correctly matched to "main", "precompartment" and "peripheral"
test_model2 = PKModel()
test_model2.create_model("main", 2, dosing_time_constant=1, elimination_time_constant=1)
test_model2.add_parent("main", "precompartment", 2, connection_time_constant=6)
test_model2.add_sibling("main", "peripheral", 2, connection_time_constant=2)
sol2 = test_model2.solve(
    np.linspace(0, 10, 10000),
    np.array(
        [
            0.0,
            0.0,
            0.0,
        ]
    ),
)
# add in part for model selection
# add in combining models

plot_solution(sol, test_model.get_compartment_names)
plot_solution(sol2, test_model.get_compartment_names)
