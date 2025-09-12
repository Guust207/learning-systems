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
     "deg2": False, "deg3": True},

    # 2
    {"lt40": True, "ge40": False, "premeno": False, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": False, "deg3": True},

    # 3
    {"lt40": False, "ge40": True, "premeno": False, "inv0-2": False, "inv3-5": False, "inv6-8": True, "deg1": False,
     "deg2": False, "deg3": True},

    # 4
    {"lt40": False, "ge40": True, "premeno": False, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": True, "deg3": False},

    # 5
    {"lt40": False, "ge40": False, "premeno": True, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": False,
     "deg2": False, "deg3": True},

    # 6
    {"lt40": False, "ge40": False, "premeno": True, "inv0-2": True, "inv3-5": False, "inv6-8": False, "deg1": True,
     "deg2": False, "deg3": False}
]

# Separate Recurrence and Non-Recurrence to two datasets
rec_patients = [patients[x] for x in (0, 2, 4)]
non_rec_patients = [patients[x] for x in (1, 3, 5)]

# Rules:
# R1: if Deg-malign 3 and not Menopause lt40 then Recurrence
# R2: if Deg-malign 3 then Recurrence
# R3: if Inv-nodes 0-2 then Non-Recurrence

forget_value = 0.9
memorize_value = 0.1

# Task 3
R1 = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 6,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 6, "NOT deg3": 5
            }
            )

R2 = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 6, "NOT deg3": 5
            }
            )

R3 = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 6, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

recurrence_rules = [R1, R2]
non_recurrence_rules = [R3]

# Task 4
print("--- Task 4 ---")
for i in range(len(patients)):
    print(
        f"Patient {i+1} classified as: {classify(patients[i], recurrence_rules, non_recurrence_rules)}."
        f" Actual: {"Recurrence " if patients[i] in rec_patients else "Non-Recurrence"}")

# Task 5
print("\n--- Task 5 ---")
# Create basic rules
forget_value = 0.8
memorize_value = 0.2

rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

non_rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

# Learn new rule for Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(rec_patients[observation_id], rec_rule)
    else:
        type_ii_feedback(non_rec_patients[observation_id], rec_rule)

print("IF " + " AND ".join(rec_rule.get_condition()) + " THEN Recurrence")

# Task 6
print("\n--- Task 6 ---")

# Learn new rule for Non-Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(non_rec_patients[observation_id], non_rec_rule)
    else:
        type_ii_feedback(rec_patients[observation_id], non_rec_rule)

print("IF " + " AND ".join(non_rec_rule.get_condition()) + " THEN Non-Recurrence")

print("\nClassifying with new learned rules")
for i in range(len(patients)):
    print(
        f"Patient {i+1} classified as: {classify(patients[i], [rec_rule], [non_rec_rule])}."
        f" Actual: {"Recurrence " if patients[i] in rec_patients else "Non-Recurrence"}"
    )

# Task 7
print("\n--- Task 7 ---")

# Learn new rule for Recurrence
forget_value = 0.5
memorize_value = 0.5

rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

non_rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

# Learn new rule for Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(rec_patients[observation_id], rec_rule)
    else:
        type_ii_feedback(non_rec_patients[observation_id], rec_rule)

print("IF " + " AND ".join(rec_rule.get_condition()) + " THEN Recurrence")

# Learn new rule for Non-Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(non_rec_patients[observation_id], non_rec_rule)
    else:
        type_ii_feedback(rec_patients[observation_id], non_rec_rule)

print("IF " + " AND ".join(non_rec_rule.get_condition()) + " THEN Non-Recurrence")

print("\nClassifying with new learned rules")
for i in range(len(patients)):
    print(
        f"Patient {i+1} classified as: {classify(patients[i], [rec_rule], [non_rec_rule])}."
        f" Actual: {"Recurrence " if patients[i] in rec_patients else "Non-Recurrence"}"
    )

# Task 8
print("\n--- Task 8 ---")

# Learn new rule for Recurrence
forget_value = 0.2
memorize_value = 0.8

rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

non_rec_rule = Memory(forget_value, memorize_value,
            {
                "lt40": 5, "NOT lt40": 5,
                "ge40": 5, "NOT ge40": 5,
                "premeno": 5, "NOT premeno": 5,
                "inv0-2": 5, "NOT inv0-2": 5,
                "inv3-5": 5, "NOT inv3-5": 5,
                "inv6-8": 5, "NOT inv6-8": 5,
                "deg1": 5, "NOT deg1": 5,
                "deg2": 5, "NOT deg2": 5,
                "deg3": 5, "NOT deg3": 5
            }
            )

# Learn new rule for Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(rec_patients[observation_id], rec_rule)
    else:
        type_ii_feedback(non_rec_patients[observation_id], rec_rule)

print("IF " + " AND ".join(rec_rule.get_condition()) + " THEN Recurrence")

# Learn new rule for Non-Recurrence
n = 100  # Number of rounds
for i in range(n):
    observation_id = random.choice(list(range(len(rec_patients))))
    choose_rec = random.choice([0, 1])  # Rec (1) or Non-Rec (0)
    if choose_rec == 1:
        type_i_feedback(non_rec_patients[observation_id], non_rec_rule)
    else:
        type_ii_feedback(rec_patients[observation_id], non_rec_rule)

print("IF " + " AND ".join(non_rec_rule.get_condition()) + " THEN Non-Recurrence")

print("\nClassifying with new learned rules")
for i in range(len(patients)):
    print(
        f"Patient {i+1} classified as: {classify(patients[i], [rec_rule], [non_rec_rule])}."
        f" Actual: {"Recurrence " if patients[i] in rec_patients else "Non-Recurrence"}"
    )