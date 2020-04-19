import pandas as pd

countries = pd.read_csv("../../processed_data/00_Country.csv", index_col=0)
df = pd.DataFrame(countries["Country"])

print(df)

