import pandas as pd

df = pd.read_csv("../../raw_data/worldcities.csv")
df = df[["country", "city", "lat", "lng"]]
df.rename(columns={"country":"Country"}, inplace=True)
df.set_index("Country", inplace=True)
df.sort_index(inplace=True)
print(df)
# df.to_csv("../../processed_data/06_lat_lng.csv")

country = pd.DataFrame(df.index)
country.drop_duplicates(inplace=True)
country["lat lng"] = True
country.set_index("Country", inplace=True)
print(country)

countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
countrycsv.pop('Unnamed: 0')
countrycsv.set_index(keys='Country', inplace=True)

print(countrycsv)
countrycsv = pd.concat([countrycsv, country], axis=1)
countrycsv.sort_index(inplace=True)
countrycsv.reset_index(inplace=True)
countrycsv.rename(columns={'index': "Country"}, inplace=True)
print(countrycsv)
# countrycsv.to_csv("../../processed_data/00_Country.csv")