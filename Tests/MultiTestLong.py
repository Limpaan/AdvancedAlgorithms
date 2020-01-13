from multiprocessing import Process, Queue, Pool
from DotSpace import DotSpace
import numpy as np
from HomExam import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Interval and dot values
    n = 500000
    d = 0.0000005
    interval_max = 1

    # Sampling values
    m_max = 5000
    gamma = 0.0
    alpha = 0.000001
    long = np.geomspace(0.25, 0.000125, 30)
    dots_list = []

    x = []
    y = []
    num_trials = 300

    for j in range(num_trials):
        dots = DotSpace(n, d, interval_max, DotSpace.NORMAL_DIST)
        dots_list.append(dots)

    for i in range(len(long)):
        pool = Pool()
        results = []
        x.append(i)
        for j in range(num_trials):
            results.append(pool.apply_async(func=ignore_long_uniform, args=(dots_list[j], m_max, gamma, alpha, long[i])))
        q1 = [result.get() for result in results]
        with open("E:\\Programming\\AdvancedAlgorithms\\longtest_run{}_alg.txt".format(i + 23), "w+") as outfile:
            tot = 0
            tot1 = 0
            for k in range(len(q1)):
                val = q1[k]
                outfile.write(str(val) + "\n")
                tot += (val - n)**2
                tot1 += math.fabs(val - n)
            outfile.write("MSE: " + str(tot / num_trials) + "\n")
            outfile.write("MAE: " + str(tot1 / num_trials) + "\n")
            outfile.write("Limit: " + str(long[i]) + "\n")
            y.append(str(tot / num_trials))
    plt.plot(x, y)
    plt.show()