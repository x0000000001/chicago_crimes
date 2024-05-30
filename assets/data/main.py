# reduce "crimes.csv" very large file into a smaller one
# by taking randomly 1 record out of 1000

import pandas as pd

data = pd.read_csv("crimes.csv")
data = data.sample(frac=0.001)
data.to_csv("crimes_reduced.csv", index=False)
