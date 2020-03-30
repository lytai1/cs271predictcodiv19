import pandas as pd

df = pd.read_csv('../../raw_data/WPP2019_TotalPopulationBySex.csv')

df.pop('LocID')
df.pop('VarID')
df.pop('Variant')
df.pop('MidPeriod')

indexName = df[df['Time'] != 2020].index
df.drop(indexName, inplace=True)
df.drop_duplicates(inplace=True)
print(df)
df.set_index(keys='Location', inplace=True)
df.to_csv('../../processed_data/03_World_Population_density.csv')

