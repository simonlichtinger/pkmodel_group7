from pkmodel.pkmodel import PKModel


# Importing all required applications/libraries
# To see the plots with titles, and axis labels as well as implemented positioning of the graph key
def plot_solution(solution, names):
    plt.figure()
    for i in range(solution.y.shape[0]):
        # plt.subplot(1,2,i,solution.t,solution.y[i,:],label=names[i])
        plt.plot(solution.t, solution.y[i, :], label=names[i])
        plt.legend(names, loc="upper left")
        plt.title("Model-title")  # place holder
        plt.ylabel("drug mass [ng]")
        plt.xlabel("time [h]")
    plt.show()


# Plot for the model types defined
# Model 1
print(type(sol))
names = ["main", "precompartment", "peripheral"]
# Display the plot
plot_solution(sol, names)
plot_solution(sol2, names)
