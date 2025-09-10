import random


class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value

    def get_memory(self):
        return self.memory

    def get_literals(self):
        return list(self.memory.keys())

    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition

    def memorize(self, literal):
        if random.random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1

    def forget(self, literal):
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1


def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in observation:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition


def classify(observation, rec_rules, non_rec_rules):
    vote_sum = 0
    for rule in rec_rules:
        if evaluate_condition(observation, rule.get_condition()):
            vote_sum += 1
    for rule in non_rec_rules:
        if evaluate_condition(observation, rule.get_condition()):
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-Recurrence"


def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            elif observation[feature] == False:
                memory.memorize('NOT ' + feature)
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals:
        memory.forget(literal)


def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)

# Task 2
patients = [
    # 1
    {"lt40": False, "ge40": True, "premeno": False, "inv0-2": False, "inv3-5": True, "inv6-8": False, "deg1": False,
     "deg2": False, "deg3": True, "rec": True},

    # 2
    {"lt40": True, "ge40": False, "premeno": False, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": False, "deg3": True, "rec": False},

    # 3
    {"lt40": False, "ge40": True, "premeno": False, "inv0-2": False, "inv3-5": False, "inv6-8": True, "deg1": False,
     "deg2": False, "deg3": True, "rec": True},

    # 4
    {"lt40": False, "ge40": True, "premeno": False, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": True, "deg3": False, "rec": False},

    # 5
    {"lt40": False, "ge40": False, "premeno": True, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": False, "deg3": True, "rec": True},

    # 6
    {"lt40": False, "ge40": False, "premeno": True, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": True,
     "deg2": False, "deg3": False, "rec": False}
]

# Rules:
# R1: if Deg-malign 3 and not Menopause lt40 then Recurrence
# R2: if Deg-malign 3 then Recurrence
# R3: if Inv-nodes 0-2 then Non-Recurrence

forget_value = 0.9
memorize_value = 0.1

# Task 3
R1 = Memory(forget_value, memorize_value,
            {"lt40": 5, "NOT lt40": 6, "ge40": 5, "NOT ge40": 5, "premeno": 5, "NOT premeno": 5, "inv0-2": 5,
             "inv3-5": 5, "inv6-8": 5, "deg1": 5, "NOT deg1": 5, "deg2": 5, "NOT deg2": 5, "deg3": 6, "NOT deg3": 5}
            )

R2 = Memory(forget_value, memorize_value,
            {"lt40": 5, "NOT lt40": 5, "ge40": 5, "NOT ge40": 5, "premeno": 5, "NOT premeno": 5, "inv0-2": 5,
             "inv3-5": 5, "inv6-8": 5, "deg1": 5, "NOT deg1": 5, "deg2": 5, "NOT deg2": 5, "deg3": 6, "NOT deg3": 5}
            )

R3 = Memory(forget_value, memorize_value,
            {"lt40": 5, "NOT lt40": 5, "ge40": 5, "NOT ge40": 5, "premeno": 5, "NOT premeno": 5, "inv0-2": 6,
             "inv3-5": 5, "inv6-8": 5, "deg1": 5, "NOT deg1": 5, "deg2": 5, "NOT deg2": 5, "deg3": 5, "NOT deg3": 5}
            )

recurrence_rules = [R1, R2]
non_recurrence_rules = [R3]

