# noinspection PyUnresolvedReferences
cimport cython
cimport numpy as np

ctypedef np.int_t DTYPE_t
ctypedef np.float_t DTYPE_f

# noinspection PyPep8Naming,PyUnresolvedReferences
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def floyd_warshall(np.ndarray[DTYPE_f, ndim=4] W, np.ndarray[DTYPE_t, ndim=5] P):
    # Classical Floyd Warshall algorithm with the precedent neighbour kept in memory to rebuild the explored paths
    n = W.shape[0]
    modified = False
    for a in range(n):
        for b in range(n):
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        for l in range(n):
                            if W[a, b, i, j] > W[a, b, k, l] + W[k, l, i, j]:
                                W[a, b, i, j] = W[a, b, k, l] + W[k, l, i, j]
                                P[a, b, i, j, 0] = k
                                P[a, b, i, j, 1] = l
                                modified = True
    return modified
