import numpy as np


def zeroth_order(t: float, q: list, k: float) -> float:
    """Simple zeroth-order rate function.

    :param t:   model time
    :param q:   Vector (list) of mass distribution through compartments (not actually used but required argument for ODE solver)
    :param k:   Time constant of the rate function.
    :returns:   Zeroth-order rate.
    """
    return k


def first_order(t: float, q: list, k: float, q_index: int) -> float:
    """Simple first-order rate function.

    :param t:       model time
    :param q:       Vector (list) of mass distribution through compartments
    :param k:       Time constant of the rate function.
    :param q_index: Index within q on which the rate depends to first order.
    :returns:       First-order rate.
    """
    return k * q[q_index]


def dose_constant(t: float, q: list, X: float) -> float:
    """Dose function for a steady, constant stream of drug dosage.

    :param t:   model time
    :param q:   Vector (list) of mass distribution through compartments (not actually used but required argument for ODE solver)
    :param X:   Constant dose applied
    :returns:   Dosing input rate to the system.
    """
    return X


def dose_steady(t: float, q: list, X: float, times: list) -> float:
    """Administers a steady dose within a fixed list of time windows.

    :param t:       model time
    :param q:       Vector (list) of mass distribution through compartments (not actually used but required argument for ODE solver)
    :param X:       dosage to be applied
    :param times:   2d list of times at which to stop and start dosage in format [[start_time_1,stop_time_1],[start_time_2,stop_time_2],...]
    :returns:       dosage flow resulting dependent on time, =X if in a time window, =0 if not.
    """

    # check times tuple is the correct shape

    if len(np.shape(times)) != 2 or np.shape(times)[1] != 2:
        raise TypeError(
            "times should be a 2d list of shape (n,2) where n is the number of doses, i.e. in the format \
    [[start_time_1,stop_time_1],[start_time_2,stop_time_2],...]"
        )

    # check if t is in within time range

    for time in times:
        if t >= time[0] and t <= time[1]:
            return X

    return 0  # Neede to add a default return of 0
