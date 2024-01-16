import constants as c
import oc as oc
import random
import matplotlib.pyplot as plt
import numpy as np
import q_learning as ql


def test():
    iterations = 1000
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

def random_games(iterations):
    points_list = []

    average_last_100_list = []
    x_list = []
    for i in range(0, iterations):
        oc.reset(2)
        points_list.append(controller())
        if i % 100 == 0 and i != 0:
            average_last_100 = 0
            for j in range(i - 100, i):
                average_last_100 += points_list[j]
            average_last_100 /= 100
            average_last_100_list.append(average_last_100)
            x_list.append(i)
            print("i:" + str(i) + " Average last 100: " + str(average_last_100))
    plt.plot(x_list, average_last_100_list)
    plt.title("Durchschnittliche Endpunktzahl der letzten 100 Spiele (Zufällig)")
    plt.ylabel("Durchschnittliche Punktzahl")
    plt.xlabel("Spiele")
    plt.show()
def train(iterations):
    points_list = []
    average_last_100_list = []
    used_q_list = []
    x_list = []
    play_points_list = []
    points_2x2 = []
    q_l = ql.q_learning(0.8, 0.02, 0.0001, 0.9, 0.9, 0.0001, 0.1)
    for i in range(0, (iterations + 1)):
        points = q_l.play_round()
        points_list.append(points)
        if i % 100 == 0 and i != 0:
            average_last_100 = 0
            for j in range(0, 99):
                average_last_100 += points_list[j]
            average_last_100 /= 100
            average_last_100_list.append(average_last_100)
            points_list = []
            all_steps = q_l.steps_with_q + q_l.steps_without_q
            used_q_list.append(q_l.steps_with_q / all_steps)
            q_l.steps_with_q = 0
            q_l.steps_without_q = 0
            x_list.append(i)
            print("i:" + str(i) + " Schrittweite: " + str(q_l.schrittweite) + " Epsilon: " + str(q_l.epsilon) + " Average last 100: " + str(average_last_100) + "Length of q_table: " + str(len(q_l.q_table)))
    plt.plot(x_list, average_last_100_list)
    plt.title("Durchschnittliche Endpunktzahl der letzten 100 Spiele (Q-Learning)")
    plt.ylabel("Durchschnittliche Punktzahl")
    plt.xlabel("Spiele")
    plt.show()
    plt.plot(x_list, used_q_list)
    plt.title("Anteil Entscheidung durch initialisierten Eintrag")
    plt.ylabel("Anteil")
    plt.xlabel("Spiele")
    plt.show()
    for k in range(0, 1000):
        points = q_l.play()
        play_points_list.append(points)
    print("Play fertig")
    for i in range(0, 1000):
        oc.reset(2)
        p = controller()
        points_2x2.append(p)
    print("2x2 fertig")
    plt.hist(points_2x2, bins=25)
    plt.title("Performance Zufällig")
    plt.show()
    plt.hist(play_points_list, bins=25)
    plt.title("Performance Q-Learning")
    plt.show()



if __name__ == '__main__':
    c.current_game = None
    #random_games(1000)
    train(10000)
