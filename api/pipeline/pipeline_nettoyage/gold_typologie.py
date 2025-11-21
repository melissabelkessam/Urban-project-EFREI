import pandas as pd

df = pd.read_csv("../data/Silver/typologie_paris.csv")

df.to_csv("../data/Gold/typologie_logements.csv", index=False)

print("Gold typologie OK ✔")
