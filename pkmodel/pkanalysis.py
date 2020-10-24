# This will hold visualisation code
import matplotlib.pyplot as plt


def plot_solution(
    solution, names, time_units="time units", mass_units="mass units", title="PK Model", testing=False
):
    """Method to plot the solution object returned by PKModel.solve() as a mass / time graph
    including different compartments.

    :param solution:        Solution object returned by PKModel.solve()
    :param names:           List of the compartment names.  Can be obtained by PKModel.get_compartment_names
    :param time_units:      (optional) Units for time to be displayed in the axis label. Default = 'time units'.
    :param mass_units:      (optional) Units for mass to be displayed in the axis label. Default = 'mass units'.
    :param title:           (optional) Title of the plot.
    :param testing:         (optional) Don't do plt.show if testing, as this fails the test if window isn't closed. Default = False.
    """

    for i in range(solution.y.shape[0]):
        plt.plot(solution.t, solution.y[i, :], label=names[i])
        plt.legend(names)
        plt.title(title)
        plt.ylabel("Drug mass [" + mass_units + "]")
        plt.xlabel("Time [" + time_units + "]")
    if not testing:
        plt.show()
