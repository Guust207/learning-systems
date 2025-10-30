import pandas as pd

pi_automatas = {"prob": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}
row_idx = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6", "pi7", "pi8",]

df = pd.DataFrame(data=pi_automatas, index=row_idx)

print(df)