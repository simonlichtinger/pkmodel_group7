# This will hold visualisation code
import matplotlib.pyplot as plt
import numpy as np


def plot_solution(solution, names):
    """Simple plot functionality

    this plots the evolution of the drug concentration and states whether equilibrium was reached
    within the simulation time

    :param solution:   solution object containing time and all concentrations
    :param names:      name of the compartment
    :returns:          plot

    """
    # Equilibrium will be considered reached if the numerical derivative is less than 0.001, this will be
    # output in the title
    numDiv = np.diff(solution.y) / np.diff(solution.t)
    LastDivElem = numDiv[:, -1]
    if all(i < 0.01 for i in LastDivElem):
        eqiFlag = "Equilibrium reached"
    else:
        eqiFlag = "Equilibrium not reached"

    for i in range(solution.y.shape[0]):
        plt.plot(solution.t, solution.y[i, :], label=names[i])
        plt.legend(names, loc="upper left")
        plt.title("Model-title" + " " + "(" + eqiFlag + ")")  # place holder
        plt.ylabel("drug mass [ng]")
        plt.xlabel("time [h]")
    plt.show()
