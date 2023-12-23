import constants as c
import oc as oc
import random
import matplotlib.pyplot as plt
import numpy as np


def test():
    iterations = 50
    index_array = []
    points_2x2 = []
    points_3x3 = []
    points_4x4 = []
    average_2x2 = 0
    average_3x3 = 0
    average_4x4 = 0
    for i in range(0, iterations):
        oc.reset(2)
        p = controller()
        points_2x2.append(p)
        average_2x2 += p
        index_array.append(i)
        #print(i)
    print("2x2 fertig")
    for i in range(0, iterations):
        oc.reset(3)
        p = controller()
        points_3x3.append(p)
        average_3x3 += p
        print(i)
    print("3x3 fertig")
    for i in range(0, iterations):
        oc.reset(4)
        p = controller()
        points_4x4.append(p)
        average_4x4 += p
        print(i)
    print("4x4 fertig")
    print(points_2x2)
    print(points_3x3)
    print(points_4x4)
    average_2x2 /= iterations
    average_3x3 /= iterations
    average_4x4 /= iterations
    plt.hist(points_2x2, bins=50)
    plt.show()
    plt.hist(points_3x3, bins=50)
    plt.show()
    plt.hist(points_4x4, bins=50)
    plt.show()
    plt.plot(index_array, points_2x2)
    plt.axhline(y = np.nanmean(points_2x2), color = 'r', linestyle = '-')
    plt.show()
    plt.plot(index_array, points_3x3)
    plt.axhline(y=np.nanmean(points_3x3), color='r', linestyle='-')
    plt.show()
    plt.plot(index_array, points_4x4)
    plt.axhline(y=np.nanmean(points_4x4), color='r', linestyle='-')
    plt.show()



def controller():
    while True:
        matrix, points, end = oc.state()
        if end:
            break
        r = random.randint(0, 4)
        if r == 0:
            oc.move("up")
        elif r == 1:
            oc.move("right")
        elif r == 2:
            oc.move("down")
        elif r == 3:
            oc.move("left")
    return c.points


if __name__ == '__main__':
    test()
