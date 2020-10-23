# This will hold visualisation code
import matplotlib.pyplot as plt
import numpy as np


def plot_solution(solution, names):
    """
    this plots the outpu of the models as the results are generated from the other


    """
    numDiv = np.diff(solution.y) / np.diff(solution.t)
    LastDivElem = numDiv[:, -1]
    if all(i < 0.001 for i in LastDivElem):
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
