# Importing all required applications/libraries
from pkmodel.pkmodel import PKModel
import matplotlib.pyplot as plt
import numpy as np
# To see the plots with titles, and axis labels as well as implemented positioning of the graph key
def plot_solution(solution, names):
    for i in range (solution.y.shape[0]):
        plt.plot(solution.t, solution.y[i,:], label = names[i])
        plt.legend (names, loc='upper left')
        plt.title('Model-title') # place holder
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
    plt.show()
# Plot for the model types defined 
test_model = PKModel()
test_model.create_model("main", 1, dosing_time_constant = 1, elimination_time_constant = 1 )  
test_model.add_parent("main", "precompartment", 1, connection_time_constant = 6 )  
test_model.add_sibling("main", "peripheral", 1, connection_time_constant = 2 ) 
sol = test_model.solve(np.linspace(0, 10, 10000), np.array([0.0, 0.0, 0.0,]))

print(type(sol))
names = ["main", "precompartment", "peripheral"]
# Display the plot 
plot_solution (sol, names)

