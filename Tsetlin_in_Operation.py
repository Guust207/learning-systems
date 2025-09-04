#!/usr/bin/python

import random

class Environment:
    def __init__(self, c_1, c_2):
        self.c_1 = c_1
        self.c_2 = c_2

    def penalty(self, action):
        if action == 1:
            if random.random() <= self.c_1:
                return True
            else:
                return False
        elif action == 2:
            if random.random() <= self.c_2:
                return True
            else:
                return False

class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n+1])

    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2*self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        elif self.state > self.n:
            self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 1
        else:
            return 2

        
env = Environment(0.1, 0.3)

la = Tsetlin(3)

action_count = [0,0]

for i in range(10000):
    action = la.makeDecision()

    action_count[action - 1] += 1
    penalty = env.penalty(action)

    print("State:", la.state,"Action:", action, end = ' ')

    if penalty:
        print("Penalty", end = ' ')
        la.penalize()
    else:
        print("Reward", end = ' ')
        la.reward()

    print("New State:", la.state)

print("#Action 1: ", action_count[0], "#Action 2:", action_count[1])
