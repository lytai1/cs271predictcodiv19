import pandas as pd

df = pd.read_csv("../../raw_data/gross-enrollment-ratio-in-tertiary-education.csv")
df.pop("Code")
df = df[df["Year"] == 2013]
df.rename(columns={"Entity":"Country"}, inplace=True)
df.set_index(keys="Country", inplace=True)
country = pd.read_csv('../../processed_data/00_Country.csv', index_col=0)
print(country)
df = df[df.index.isin(country["Country"])]

print(df)
# df.to_csv("../../processed_data/07_education.csv")

#add country name to csv
country = pd.DataFrame(df.index)
country.drop_duplicates(inplace=True)
country.set_index(keys='Country', inplace=True)
country["Tertiary Education"] = True
print(country)

countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
countrycsv.pop('Unnamed: 0')
countrycsv.set_index(keys='Country', inplace=True)
countrycsv = pd.concat([countrycsv, country], axis=1)
print(countrycsv)

countrycsv.sort_index(inplace=True)
countrycsv.reset_index(inplace=True)
countrycsv.rename(columns={'index': "Country"}, inplace=True)

print(countrycsv)
# countrycsv.to_csv("../../processed_data/00_Country.csv")