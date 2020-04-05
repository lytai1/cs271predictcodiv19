import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('../../raw_data/GDP_PPP.xlsx')

df.pop('Scale')
df.pop('Estimates Start After')
df.pop('Country/Series-specific Notes')

#make 01_GDP.csv
indexName = df[df['Subject Descriptor'] == 'Gross domestic product based on purchasing-power-parity (PPP) share of world total'].index
gdp = df.drop(indexName, inplace=False)
gdp.pop('Subject Descriptor')
country = pd.DataFrame(gdp['Country'])
country.reset_index(drop=True, inplace=True)
country["GDP"] = True
country["PPP"] = True
print(country)
country.to_csv('../../processed_data/00_Country.csv') #print list of country as csv
gdp.set_index(keys='Country', inplace=True)
print(gdp)
gdp.to_csv('../../processed_data/01_GDP.csv')

#make 02_PPP.csv
indexName = df[df['Subject Descriptor'] != 'Gross domestic product based on purchasing-power-parity (PPP) share of world total'].index
ppp = df.drop(indexName, inplace=False)
ppp.pop('Subject Descriptor')
ppp.set_index(keys='Country', inplace=True)
print(ppp)
ppp.to_csv('../../processed_data/02_PPP.csv')

