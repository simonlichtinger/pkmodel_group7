# This will hold visualisation code
import matplotlib.pyplot as plt


def plot_solution(solution, names):
    for i in range(solution.y.shape[0]):
        plt.plot(solution.t, solution.y[i, :], label=names[i])
        plt.legend(names, loc="upper left")
        plt.title("Model-title")  # place holder
        plt.ylabel("drug mass [ng]")
        plt.xlabel("time [h]")
    plt.show()

    # doc string
    # test
