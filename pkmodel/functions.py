import numpy as np

zeroth_order = lambda t,q,k: k
first_order = lambda t,q,k,q_index: k*q[q_index]


def dose_constant(t,X):
    return X


def dose_steady(t,X,times):
    """Administers a steady dose between two times.
    
    :param t:       model time
    :param X:       dosage in ng
    :param times:   2d list of times at which to stop and start dosage in format [[start_time_1,stop_time_1],[start_time_2,stop_time_2],...]
    :returns:       dosage in ng
    """

    # check times tuple is the correct shape

    if len(np.shape(times)) != 2 or np.shape(times)[1] != 2:
        raise TypeError('times should be a 2d list of shape (n,2) where n is the number of doses, i.e. in the format \
    [[start_time_1,stop_time_1],[start_time_2,stop_time_2],...]')

    # check if t is in within time range

    for time in times:
        if t>=time[0] and t<=time[1]:
            return X





