import pandas as pd

df = pd.read_csv('../../raw_data/WPP2019_TotalPopulationBySex.csv')

df.pop('LocID')
df.pop('VarID')
df.pop('Variant')
df.pop('MidPeriod')

indexName = df[df['Time'] != 2020].index
df.drop(indexName, inplace=True)
df.drop_duplicates(inplace=True)

df.set_index(keys='Location', inplace=True)
print(df)
# df.to_csv('../../processed_data/03_World_Population_density.csv')

#add country name to csv
country = pd.DataFrame(df.index)
country.rename(columns={'Location': "Country"}, inplace=True)
country.set_index(keys='Country', inplace=True)
country["population density"] = True
print(country)
countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
countrycsv.pop('Unnamed: 0')
countrycsv.set_index(keys='Country', inplace=True)

print(countrycsv)
countrycsv = pd.concat([countrycsv, country], axis=1)
countrycsv.reset_index(inplace=True)
countrycsv.rename(columns={'index': "Country"}, inplace=True)
print(countrycsv)
countrycsv.to_csv("../../processed_data/00_Country.csv")

