import oc
from random import random, randint

class q_learning:
    def __init__(self, schrittweite_start, schrittweite_stop, schrittweite_step, gamma, epsilon_start, epsilon_step, epsilon_stop):
        self.schrittweite = schrittweite_start
        self.schrittweite_stop = schrittweite_stop
        self.schrittweite_step = schrittweite_step
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_step = epsilon_step
        self.epsilon_stop = epsilon_stop
        self.q_table = []
        self.steps_with_q = 0
        self.steps_without_q = 0

    def train(self, iterations):
        for i in range(0, iterations):
            points = self.play_round()
            print(str(i) + ": " + str(points))
        

    def play(self):
        def get_best_action(row):
            for i in range(0, 4):
                if row.q_values[i] == max(row.q_values):
                    return i
        oc.reset(2)
        matrix1 = ([1,1],[1,1])
        matrix, points, end = oc.state()
        
        while not end:
            row = self.find_new_row(matrix)
            action = get_best_action(row)
            if matrix == matrix1:
                return points
            else:
                if action == 0:
                    oc.move("up")
                elif action == 1:
                    oc.move("right")
                elif action == 2:
                    oc.move("down")
                elif action == 3:
                    oc.move("left")
                else:
                    print("Error")
            matrix1 = matrix
            matrix, points, end = oc.state()
        return points


    def play_round(self):
        def get_best_action(row):
            for i in range(0, 4):
                if row.q_values[i] == max(row.q_values):
                    return i
        oc.reset(2)
        matrix, points, end = oc.state()
        
        new_row = self.find_new_row(matrix)
        if new_row == None:
            new_row = q_row(matrix)
            self.q_table.append(new_row)
            self.steps_without_q += 1
        else:
            self.steps_with_q += 1
        row = new_row
        while not end:
            randNum = random()
            if randNum < self.epsilon:
                action = randint(0, 3)
            else:
                action = get_best_action(row)
            if action == 0:
                oc.move("up")
            elif action == 1:
                oc.move("right")
            elif action == 2:
                oc.move("down")
            elif action == 3:
                oc.move("left")
            new_matrix, new_points, end = oc.state()
            if not end:
                new_row = self.find_new_row(new_matrix)
                if new_row == None:
                    new_row = q_row(new_matrix)
                    self.q_table.append(new_row)
                    self.steps_without_q += 1
                else:
                    self.steps_with_q += 1
                row.q_values[action] += self.schrittweite * ((new_points - points) + self.gamma * max(new_row.q_values) - row.q_values[action])
                row = new_row
                matrix = new_matrix
                points = new_points
        self.epsilon -= self.epsilon_step
        if self.epsilon < self.epsilon_stop:
            self.epsilon = self.epsilon_stop
        self.schrittweite -= self.schrittweite_step
        if self.schrittweite < self.schrittweite_stop:
            self.schrittweite = self.schrittweite_stop
        return points


    def find_new_row(self, matrix):
        for row in self.q_table:
            if row.matrix == matrix:
                return row
        return None


class q_row:
    def __init__(self, matrix):
        self.matrix = matrix
        self.points = 0
        self.q_values = [0, 0, 0, 0]