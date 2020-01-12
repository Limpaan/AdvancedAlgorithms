from multiprocessing import Process, Queue
from DotSpace import DotSpace
from HomExam import *


def run_function1(f, q, dots, m_max, gamma, alpha):
    ret = f(dots, m_max, gamma, alpha)
    q.put(ret)


def run_function2(f, q, dots, m_max, gamma, alpha, long):
    ret = f(dots, m_max, gamma, alpha, long)
    q.put(ret)


if __name__ == '__main__':
    # Interval and dot values
    n = [10000, 50000, 100000, 500000, 1000000]
    d = 0.0000005
    interval_max = 1

    # Sampling values
    m_max = 5000
    gamma = 0.0
    alpha = 0.000001
    long = 0.0137

    for i in range(5):
        q1 = Queue()
        q2 = Queue()
        thread_list = []
        for j in range(100):
            dots = DotSpace(n[i], d, interval_max, DotSpace.NORMAL_DIST)
            p1 = Process(target=run_function1, args=(pure_uniform, q1, dots, m_max, gamma, alpha))
            p2 = Process(target=run_function2, args=(ignore_long_uniform, q2, dots, m_max, gamma, alpha, long))
            p1.start()
            p2.start()
            thread_list.append(p1)
            thread_list.append(p2)
        for j in range(len(thread_list)):
            thread_list[j].join()
        with open("E:\\Programming\\AdvancedAlgorithms\\run{}_alg{}.txt".format(i, 1), "w+") as outfile:
            tot = 0
            tot1 = 0
            for _ in range(q1.qsize()):
                val = q1.get()
                outfile.write(str(val) + "\n")
                tot += (val - n[i])**2
                tot1 += math.fabs(val - n[1])
            outfile.write("MSE: " + str(tot / 100))
            outfile.write("MAE: " + str(tot1 / 100))
        with open("E:\\Programming\\AdvancedAlgorithms\\run{}_alg{}.txt".format(i, 2), "w+") as outfile:
            tot = 0
            tot1 = 0
            for _ in range(q2.qsize()):
                val = q2.get()
                outfile.write(str(val) + "\n")
                tot += (val - n[i]) ** 2
                tot1 += math.fabs(val - n[1])
            outfile.write("MSE: " + str(tot / 100))
            outfile.write("MAE: " + str(tot1 / 100))
