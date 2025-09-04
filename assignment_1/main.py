# Goore game
# 5 independent automatas, voting yes or no
# Goal of a round is to get exactly 3 "YES" votes
#
# Rewards:
# 0 --> 0
# 1 --> 0.2
# 2 --> 0.4
# 3 --> 0.6
# 4 --> 0.4
# 5 --> 0.2

# Actions:
# 0 --> "No"
# 1 --> "Yes"

import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n+1])

    def reward(self):
        if self.n >= self.state > 1:
            self.state -= 1
        elif 2*self.n > self.state > self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        elif self.state > self.n:
            self.state -= 1

    def make_decision(self):
        if self.state <= self.n:
            return 0
        else:
            return 1

ta_list = []
for i in range(5):
    ta_list.append(Tsetlin(5))

epochs = []
total_M = []
state_overview = []
no_wins = 0
no_rounds = 10000

for i in range(no_rounds):
    current_states = []
    M = 0
    for ta in ta_list:
        M += ta.make_decision()

    if M < 4:
        reward_chance = M * 0.2
    else:
        reward_chance = 0.6 - (M - 3) * 0.2

    for ta in ta_list:
        if random.random() <= reward_chance:
            ta.reward()
        else:
            ta.penalize()

        current_states.append(ta.state)

    epochs.append(i)
    total_M.append(M)
    state_overview.append(current_states)

    # Check "win"
    if M == 3:
        no_wins += 1

for i in range(len(ta_list)):
    action = "Yes" if ta_list[i].make_decision() else "No"
    print(f"Tsetlin Automata {i+1} final state: {ta_list[i].state} ({action})")

print(f"\nWin rate: {no_wins} wins of {no_rounds} rounds. ({(no_wins / no_rounds) * 100:.1f}%)")

df = pd.DataFrame({'Epochs': epochs, 'M': total_M})
window_size = max(1, int(len(df) * 0.02))
df['Rolling_M'] = df['M'].rolling(window=window_size, center=True).mean()

plt.figure(figsize=(10, 6))
plt.plot(df['Epochs'], df['M'], label='Original', color='blue', alpha=0.5)
plt.plot(df['Epochs'], df['Rolling_M'], label=f'Rolling Avg ({window_size} epochs)', color='red', linewidth=2)

plt.xlabel('Epochs')
plt.ylabel('M')
plt.title('Epochs vs M with Rolling Average')
plt.legend()
plt.grid(True)
plt.show()



episodes = list(range(1, len(state_overview) + 1))

# Number of series
num_series = len(state_overview[0])

# Calculate step for 10% sampling
total_episodes = len(episodes)
step = max(1, total_episodes // 10)

# Downsample episodes and data
sampled_episodes = episodes[::step]
sampled_data = state_overview[::step]

# Plot
plt.figure(figsize=(10, 6))

for i in range(num_series):
    y_values = [row[i] for row in sampled_data]
    markers = ['o', 's', '^', 'D', 'x']
    plt.scatter(sampled_episodes, y_values, marker=markers[i % len(markers)], alpha=0.7, label=f'Graph {i + 1}')

plt.axhline(y=5, color='gray', linestyle='--', linewidth=1.5, label='y = 5')

# Labels and title
plt.xlabel('Epochs')
plt.ylabel('M')
plt.title('Current state at 10% of total epochs (Greater than 5 is "YES")')
plt.legend()
plt.grid(True)
plt.show()
