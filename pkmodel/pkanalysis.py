# This will hold visualisation code
import matplotlib.pyplot as plt


def plot_solution(solution, names, time_units="time units", mass_units="mass units", title="PK Model"):
    for i in range(solution.y.shape[0]):
        plt.plot(solution.t, solution.y[i, :], label=names[i])
        plt.legend(names)
        plt.title(title)  # place holder
        plt.ylabel("Drug mass ["+mass_units+"]")
        plt.xlabel("Time ["+time_units+"]")
    plt.show()

    # doc string
    # test
