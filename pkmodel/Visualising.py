from pkmodel.pkmodel import PKModel
import matplotlib.pyplot as plt
import numpy as np
#Importing all required applications/libraries
# To see the plots with titles, and axis labels as well as implemented positioning of the graph key
def plot_solution(solution, names):
    plt.figure()
    for i in range(solution.y.shape[0]):
        #plt.subplot(1,2,i,solution.t,solution.y[i,:],label=names[i])
        plt.plot(solution.t,solution.y[i,:],label=names[i])
        plt.legend(names, loc='upper left')
        plt.title('Model-title')#place holder
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
    plt.show()
# Plot for the model types defined
# Model 1
test_model=PKModel()
test_model.create_model("main",1,dosing_time_constant=1,elimination_time_constant=1)  
test_model.add_parent("main","precompartment",1,connection_time_constant=6)
test_model.add_sibling("main","peripheral",1,connection_time_constant=2)
sol=test_model.solve(np.linspace(0,10,10000),np.array([0.0,0.0,0.0,]))
#Model 2 --- It appears as tho the three compartment model has not been added in
#There is not sufficient info in Scipy.integrate file to allow model graphical presentation to be model presentable at the moment
#Therefore the graph being produced is only one type for both models
#It is not cleare if the allocated comparments are correctly matched to "main", "precompartment" and "peripheral"
test_model2.create_model("main",2,dosing_time_constant=1,elimination_time_constant=1)  
test_model2.add_parent("main","precompartment",2,connection_time_constant=6)
test_model2.add_sibling("main","peripheral",2,connection_time_constant=2)
sol2=test_model2.solve(np.linspace(0,10,10000),np.array([0.0,0.0,0.0,]))
# add in part for model selection
# add in combining models
print(type(sol))
names=["main","precompartment","peripheral"]
# Display the plot 
plot_solution(sol, names)
plot_solution(sol2, names)
